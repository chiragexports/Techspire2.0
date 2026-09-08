from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Course, Category, Module, Chapter
from payments.models import PaymentOrder, Payment, WebhookEvent
from payments.services import RazorpayService
from progress.models import Enrollment

User = get_user_model()

class PaymentAndAccessControlTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='student1',
            email='student1@techspire.io',
            password='Password123!',
            first_name='Alex',
            last_name='Rivera'
        )
        self.category = Category.objects.create(name='Computer Science', slug='cs')
        self.course = Course.objects.create(
            title='Python Programming Mastery',
            slug='python-mastery',
            category=self.category,
            price_in_paise=149900,
            original_price_in_paise=199900,
            is_free=False,
            is_published=True
        )
        self.module = Module.objects.create(course=self.course, title='Module 1', order=1)
        self.preview_chapter = Chapter.objects.create(
            module=self.module,
            title='Intro to Python',
            slug='intro-python',
            order=1,
            is_free_preview=True,
            content_markdown='# Free Preview'
        )
        self.paid_chapter = Chapter.objects.create(
            module=self.module,
            title='Advanced Metaprogramming',
            slug='advanced-meta',
            order=2,
            is_free_preview=False,
            content_markdown='# Secret Metaprogramming'
        )

    def test_course_pricing_properties(self):
        self.assertEqual(self.course.price_in_rupees, 1499)
        self.assertEqual(self.course.original_price_in_rupees, 1999)
        self.assertEqual(self.course.discount_amount_in_rupees, 500)
        self.assertEqual(self.course.discount_percentage, 25)

    def test_unauthenticated_and_unpaid_access_control(self):
        # 1. Preview chapter is accessible
        res = self.client.get(f'/api/courses/{self.course.slug}/chapters/{self.preview_chapter.slug}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # 2. Paid chapter is gated with 403
        res = self.client.get(f'/api/courses/{self.course.slug}/chapters/{self.paid_chapter.slug}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data.get('code'), 'payment_required')

        # 3. Authenticate user without enrollment -> still 403 on paid chapter
        self.client.force_authenticate(user=self.user)
        res = self.client.get(f'/api/courses/{self.course.slug}/chapters/{self.paid_chapter.slug}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_server_side_order_creation(self):
        self.client.force_authenticate(user=self.user)
        # Attempt to tamper amount
        res = self.client.post('/api/payments/create-order/', {
            'course_id': self.course.id,
            'amount': 1  # Malicious attempted amount of 1 rupee
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Verify server ignored client amount and strictly used course.price_in_paise
        self.assertEqual(res.data['amount'], 149900)
        self.assertEqual(res.data['amount_in_rupees'], 1499)
        self.assertTrue(PaymentOrder.objects.filter(razorpay_order_id=res.data['order_id'], amount=149900).exists())

    def test_payment_verification_and_course_unlock(self):
        self.client.force_authenticate(user=self.user)
        # 1. Create order
        order = RazorpayService.create_order(self.user, self.course)
        
        # 2. Verify with valid signature
        res = self.client.post('/api/payments/verify/', {
            'razorpay_order_id': order.razorpay_order_id,
            'razorpay_payment_id': 'pay_test_99887766',
            'razorpay_signature': 'test_valid_signature'
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data['success'])

        # 3. Check enrollment is active and paid
        enrollment = Enrollment.objects.get(user=self.user, course=self.course)
        self.assertTrue(enrollment.paid)
        self.assertEqual(enrollment.status, 'active')
        self.assertEqual(enrollment.purchase_price_in_paise, 149900)

        # 4. Paid chapter is now unlocked!
        res = self.client.get(f'/api/courses/{self.course.slug}/chapters/{self.paid_chapter.slug}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('Secret Metaprogramming', res.data['content_markdown'])

    def test_idempotent_webhook_processing(self):
        order = RazorpayService.create_order(self.user, self.course)
        payload = {
            'event_id': 'evt_test_12345',
            'event': 'payment.captured',
            'payload': {
                'payment': {
                    'entity': {
                        'id': 'pay_webhook_9999',
                        'order_id': order.razorpay_order_id,
                        'amount': 149900,
                        'method': 'upi'
                    }
                }
            }
        }
        import json
        raw_body = json.dumps(payload).encode('utf-8')

        # First webhook delivery
        res = self.client.post(
            '/api/payments/webhook/',
            data=raw_body,
            content_type='application/json',
            HTTP_X_RAZORPAY_SIGNATURE='test_webhook_valid_signature'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(Payment.objects.filter(razorpay_payment_id='pay_webhook_9999').exists())
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course, paid=True).exists())

        # Second duplicate webhook delivery (must be idempotent)
        res2 = self.client.post(
            '/api/payments/webhook/',
            data=raw_body,
            content_type='application/json',
            HTTP_X_RAZORPAY_SIGNATURE='test_webhook_valid_signature'
        )
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(Payment.objects.filter(razorpay_payment_id='pay_webhook_9999').count(), 1)
