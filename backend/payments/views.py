import json
import logging
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PaymentOrder, Payment, WebhookEvent
from .services import RazorpayService, RAZORPAY_KEY_ID
from .serializers import (
    PaymentOrderResponseSerializer,
    PaymentHistorySerializer,
    AdminPaymentSerializer
)
from courses.models import Course
from progress.models import Enrollment
from progress.services import CourseCompletionService
from accounts.permissions import IsTechspireAdmin

logger = logging.getLogger(__name__)

class CreatePaymentOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        course_id = request.data.get('course_id') or request.data.get('course_slug')
        if not course_id:
            return Response({'error': 'course_id or course_slug is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if str(course_id).isdigit():
                course = Course.objects.get(id=int(course_id), is_published=True)
            else:
                course = Course.objects.get(slug=course_id, is_published=True)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found or is unpublished.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if student already has active paid enrollment
        existing_enrollment = Enrollment.objects.filter(
            user=request.user,
            course=course,
            status='active',
            paid=True
        ).first()

        if existing_enrollment:
            return Response({
                'already_enrolled': True,
                'message': 'You already own this course.',
                'course_slug': course.slug
            }, status=status.HTTP_200_OK)

        # If course is marked Free, enroll directly without payment
        if course.is_free or course.price_in_paise == 0:
            enrollment, _ = Enrollment.objects.get_or_create(
                user=request.user,
                course=course,
                defaults={'status': 'active', 'paid': True, 'purchase_price_in_paise': 0}
            )
            CourseCompletionService.get_or_create_course_progress(request.user, course)
            return Response({
                'is_free': True,
                'enrolled': True,
                'message': 'Enrolled in free course successfully.',
                'course_slug': course.slug
            }, status=status.HTTP_200_OK)

        # Create Razorpay order on backend
        payment_order = RazorpayService.create_order(request.user, course)

        return Response({
            'order_id': payment_order.razorpay_order_id,
            'amount': payment_order.amount,
            'amount_in_rupees': payment_order.amount_in_rupees,
            'currency': payment_order.currency,
            'key_id': RAZORPAY_KEY_ID,
            'course_title': course.title,
            'course_slug': course.slug,
            'user_name': request.user.get_full_name() or request.user.username,
            'user_email': request.user.email
        }, status=status.HTTP_201_CREATED)

class VerifyPaymentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')

        if not razorpay_order_id or not razorpay_payment_id:
            return Response({
                'error': 'razorpay_order_id and razorpay_payment_id are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 1. Fetch order stored in our database for this specific user
        try:
            payment_order = PaymentOrder.objects.select_related('course', 'user').get(
                razorpay_order_id=razorpay_order_id,
                user=request.user
            )
        except PaymentOrder.DoesNotExist:
            return Response({
                'error': 'Payment order not found or does not belong to the authenticated user.'
            }, status=status.HTTP_404_NOT_FOUND)

        # 2. Verify server-side HMAC signature
        is_valid = RazorpayService.verify_signature(
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature or ''
        )

        if not is_valid:
            logger.warning(f"Invalid payment signature attempt by user {request.user.id} for order {razorpay_order_id}")
            payment_order.status = 'failed'
            payment_order.save(update_fields=['status', 'updated_at'])
            return Response({
                'error': 'Payment signature verification failed. Course access not granted.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 3. Capture payment and unlock course access idempotently
        payment, enrollment = RazorpayService.process_successful_payment(
            payment_order=payment_order,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature or '',
            method=request.data.get('method', 'razorpay')
        )

        return Response({
            'success': True,
            'message': 'Payment successfully verified. Course unlocked.',
            'course_title': payment_order.course.title,
            'course_slug': payment_order.course.slug,
            'payment_id': payment.razorpay_payment_id,
            'amount_in_rupees': payment.amount_in_rupees,
            'status': 'PAID'
        }, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        signature = request.headers.get('X-Razorpay-Signature', '')
        raw_body = request.body

        # Verify signature
        if not RazorpayService.verify_webhook_signature(raw_body, signature):
            logger.warning("Unauthorized Razorpay webhook attempt received.")
            return Response({'error': 'Invalid webhook signature.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = json.loads(raw_body.decode('utf-8'))
        except Exception:
            return Response({'error': 'Invalid JSON body.'}, status=status.HTTP_400_BAD_REQUEST)

        event_id = payload.get('event_id') or payload.get('id') or f"evt_{timezone.now().timestamp()}"
        event_type = payload.get('event', 'unknown')

        # Record webhook event idempotently
        webhook_event, created = WebhookEvent.objects.get_or_create(
            event_id=event_id,
            defaults={'event_type': event_type, 'payload': payload}
        )

        if not created and webhook_event.processed:
            return Response({'status': 'already processed'}, status=status.HTTP_200_OK)

        # Process payload event
        try:
            if event_type in ['payment.captured', 'order.paid']:
                payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
                order_id = payment_entity.get('order_id')
                payment_id = payment_entity.get('id')

                if order_id and payment_id:
                    payment_order = PaymentOrder.objects.filter(razorpay_order_id=order_id).first()
                    if payment_order:
                        RazorpayService.process_successful_payment(
                            payment_order=payment_order,
                            razorpay_payment_id=payment_id,
                            method=payment_entity.get('method', 'webhook'),
                            payload_data=payment_entity
                        )

            elif event_type == 'payment.failed':
                payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
                order_id = payment_entity.get('order_id')
                if order_id:
                    PaymentOrder.objects.filter(razorpay_order_id=order_id).update(status='failed')

            webhook_event.processed = True
            webhook_event.save(update_fields=['processed'])
        except Exception as e:
            logger.error(f"Error handling webhook event {event_id}: {e}")

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

class StudentPaymentHistoryView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentHistorySerializer
    pagination_class = None

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related('course', 'payment_order').order_by('-created_at')

class AdminPaymentListView(generics.ListAPIView):
    permission_classes = (IsTechspireAdmin,)
    serializer_class = AdminPaymentSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Payment.objects.all().select_related('user', 'course', 'payment_order').order_by('-created_at')
        
        search = self.request.query_params.get('search', '').strip()
        status_filter = self.request.query_params.get('status', '').strip()
        course_id = self.request.query_params.get('course_id', '').strip()

        if search:
            qs = qs.filter(
                Q(razorpay_payment_id__icontains=search) |
                Q(payment_order__razorpay_order_id__icontains=search) |
                Q(user__email__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(course__title__icontains=search)
            )

        if status_filter:
            qs = qs.filter(status=status_filter)

        if course_id and course_id.isdigit():
            qs = qs.filter(course_id=int(course_id))

        return qs

class AdminPaymentStatsView(APIView):
    permission_classes = (IsTechspireAdmin,)

    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Revenue aggregations
        total_rev_paise = Payment.objects.filter(status='captured').aggregate(total=Sum('amount'))['total'] or 0
        today_rev_paise = Payment.objects.filter(status='captured', created_at__gte=today_start).aggregate(total=Sum('amount'))['total'] or 0
        month_rev_paise = Payment.objects.filter(status='captured', created_at__gte=month_start).aggregate(total=Sum('amount'))['total'] or 0

        total_orders = PaymentOrder.objects.count()
        successful_payments = Payment.objects.filter(status='captured').count()
        failed_payments = PaymentOrder.objects.filter(status='failed').count()
        paid_enrollments = Enrollment.objects.filter(paid=True, status='active').count()

        # Top selling courses
        top_courses = Payment.objects.filter(status='captured').values(
            'course__id', 'course__title', 'course__slug'
        ).annotate(
            total_sales=Count('id'),
            revenue=Sum('amount')
        ).order_by('-total_sales')[:6]

        top_selling_data = [
            {
                'course_id': c['course__id'],
                'course_title': c['course__title'],
                'course_slug': c['course__slug'],
                'total_sales': c['total_sales'],
                'revenue_in_rupees': (c['revenue'] or 0) // 100
            }
            for c in top_courses
        ]

        return Response({
            'total_revenue_in_rupees': total_rev_paise // 100,
            'today_revenue_in_rupees': today_rev_paise // 100,
            'month_revenue_in_rupees': month_rev_paise // 100,
            'total_orders': total_orders,
            'successful_payments': successful_payments,
            'failed_payments': failed_payments,
            'paid_enrollments': paid_enrollments,
            'top_selling_courses': top_selling_data
        })
