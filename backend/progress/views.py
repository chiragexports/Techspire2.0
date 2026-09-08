from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Avg
from .models import Enrollment, ChapterProgress, ModuleProgress, CourseProgress
from .services import CourseCompletionService
from .serializers import EnrollmentSerializer, ChapterProgressSerializer
from courses.models import Course, Chapter
from assessments.models import AssessmentAttempt
from certificates.models import Certificate

class EnrollCourseView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, course_id_or_slug):
        try:
            if str(course_id_or_slug).isdigit():
                course = Course.objects.get(id=course_id_or_slug, is_published=True)
            else:
                course = Course.objects.get(slug=course_id_or_slug, is_published=True)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        # If course is paid and user is not admin/staff, require payment checkout
        if not course.is_free and course.price_in_paise > 0 and not (request.user.is_staff or getattr(request.user, 'role', '') == 'admin'):
            existing_paid = Enrollment.objects.filter(user=request.user, course=course, paid=True, status='active').first()
            if not existing_paid:
                return Response({
                    'error': 'This is a paid technical credential. Please complete checkout to enroll.',
                    'code': 'payment_required',
                    'price_in_rupees': course.price_in_rupees,
                    'price_in_paise': course.price_in_paise,
                    'course_slug': course.slug
                }, status=status.HTTP_402_PAYMENT_REQUIRED)

        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'status': 'active', 'paid': True, 'purchase_price_in_paise': course.price_in_paise if course.is_free else 0}
        )

        # Initialize CourseProgress
        CourseCompletionService.get_or_create_course_progress(request.user, course)

        return Response({
            'message': 'Enrolled successfully.' if created else 'Already enrolled.',
            'enrollment': EnrollmentSerializer(enrollment, context={'request': request}).data
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class MyCoursesListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EnrollmentSerializer
    pagination_class = None

    def get_queryset(self):
        # Reconcile progress for user
        enrollments = Enrollment.objects.filter(user=self.request.user, paid=True).select_related('course', 'course__category')
        for e in enrollments:
            CourseCompletionService.get_or_create_course_progress(self.request.user, e.course)
        return enrollments

class MarkChapterProgressView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        chapter_id = request.data.get('chapter_id')
        is_completed = request.data.get('is_completed', True)

        if not chapter_id:
            return Response({'error': 'chapter_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            chapter = Chapter.objects.select_related('module__course').get(id=chapter_id)
        except Chapter.DoesNotExist:
            return Response({'error': 'Chapter not found.'}, status=status.HTTP_404_NOT_FOUND)

        course = chapter.module.course

        # Verify active paid enrollment
        if not course.is_free and not (request.user.is_staff or getattr(request.user, 'role', '') == 'admin'):
            enrollment = Enrollment.objects.filter(user=request.user, course=course, paid=True, status='active').first()
            if not enrollment:
                return Response({
                    'error': 'Active paid enrollment required to mark lesson progress.',
                    'code': 'payment_required'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            enrollment = Enrollment.objects.filter(user=request.user, course=course).first()

        # Use CourseCompletionService as single authoritative engine
        course_prog = CourseCompletionService.mark_chapter(
            user=request.user,
            chapter=chapter,
            is_completed=bool(is_completed)
        )

        return Response({
            'success': True,
            'is_completed': bool(is_completed),
            'chapter_id': chapter.id,
            'course_progress_percentage': course_prog.percentage,
            'is_course_completed': course_prog.is_completed,
            'enrollment_status': enrollment.status if enrollment else 'active'
        })

class CourseProgressStatusView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_slug):
        try:
            course = Course.objects.get(slug=course_slug)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        course_prog = CourseCompletionService.get_or_create_course_progress(request.user, course)
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()

        completed_chapter_ids = list(ChapterProgress.objects.filter(
            user=request.user,
            chapter__module__course=course,
            is_completed=True
        ).values_list('chapter_id', flat=True))

        return Response({
            'is_enrolled': enrollment is not None,
            'enrollment_status': enrollment.status if enrollment else None,
            'progress_percentage': course_prog.percentage,
            'is_completed': course_prog.is_completed,
            'completed_chapters': completed_chapter_ids,
            'total_chapters': course_prog.total_chapters_count
        })

class StudentDashboardOverviewView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__category').order_by('-last_accessed_at')
        
        # Ensure all enrollments have up-to-date CourseProgress
        for e in enrollments:
            CourseCompletionService.get_or_create_course_progress(user, e.course)

        active_enrollment = enrollments.filter(status='active').first() or enrollments.first()
        active_course_data = None
        if active_enrollment:
            active_course_data = EnrollmentSerializer(active_enrollment, context={'request': request}).data

        # Overall Stats
        total_enrolled = enrollments.count()
        completed_courses = CourseProgress.objects.filter(user=user, is_completed=True).count()
        certificates_earned = Certificate.objects.filter(user=user, is_valid=True).count()
        
        # Assessment score average
        avg_score = AssessmentAttempt.objects.filter(user=user).aggregate(avg=Avg('percentage'))['avg'] or 0.0

        # Recent activities
        recent_chapters = ChapterProgress.objects.filter(
            user=user, is_completed=True
        ).select_related('chapter', 'chapter__module__course').order_by('-completed_at')[:6]

        activity_feed = [
            {
                'id': p.id,
                'chapter_title': p.chapter.title,
                'course_title': p.chapter.module.course.title,
                'course_slug': p.chapter.module.course.slug,
                'chapter_slug': p.chapter.slug,
                'completed_at': p.completed_at
            }
            for p in recent_chapters
        ]

        return Response({
            'user': {
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'email': user.email,
                'headline': user.headline,
                'avatar': user.avatar,
                'created_at': user.created_at,
            },
            'stats': {
                'total_enrolled': total_enrolled,
                'completed_courses': completed_courses,
                'certificates_earned': certificates_earned,
                'average_score': round(avg_score, 1),
                'learning_streak_days': 7,
            },
            'continue_learning': active_course_data,
            'enrolled_courses': EnrollmentSerializer(enrollments[:6], many=True, context={'request': request}).data,
            'recent_activity': activity_feed
        })
