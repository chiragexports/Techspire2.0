from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg
from courses.models import Course, Chapter
from progress.models import Enrollment, ChapterProgress
from assessments.models import AssessmentAttempt
from certificates.models import Certificate
from accounts.permissions import IsTechspireAdmin

User = get_user_model()

class AdminAnalyticsOverviewView(APIView):
    permission_classes = (IsTechspireAdmin,)

    def get(self, request):
        total_students = User.objects.filter(role='student').count()
        total_courses = Course.objects.count()
        total_chapters = Chapter.objects.count()
        total_enrollments = Enrollment.objects.count()
        total_completed_enrollments = Enrollment.objects.filter(status='completed').count()
        total_certificates = Certificate.objects.filter(is_valid=True).count()
        total_attempts = AssessmentAttempt.objects.count()
        passed_attempts = AssessmentAttempt.objects.filter(passed=True).count()

        pass_rate = round((passed_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0
        completion_rate = round((total_completed_enrollments / total_enrollments * 100), 1) if total_enrollments > 0 else 0

        # Top courses by popularity
        top_courses = Course.objects.annotate(
            student_count=Count('enrollments')
        ).order_by('-student_count')[:6].values('id', 'title', 'slug', 'student_count', 'difficulty', 'estimated_hours')

        # Recent activities
        recent_enrollments = Enrollment.objects.select_related('user', 'course').order_by('-enrolled_at')[:8]
        recent_activity_data = [
            {
                'id': e.id,
                'user_name': e.user.get_full_name() or e.user.username,
                'user_email': e.user.email,
                'course_title': e.course.title,
                'status': e.status,
                'enrolled_at': e.enrolled_at
            }
            for e in recent_enrollments
        ]

        recent_certs = Certificate.objects.select_related('user', 'course').order_by('-issue_date')[:6]
        recent_certs_data = [
            {
                'id': str(c.id),
                'certificate_code': c.certificate_code,
                'student_name': c.user.get_full_name() or c.user.username,
                'course_title': c.course.title,
                'grade_percentage': c.grade_percentage,
                'issue_date': c.issue_date
            }
            for c in recent_certs
        ]

        return Response({
            'metrics': {
                'total_students': total_students,
                'total_courses': total_courses,
                'total_chapters': total_chapters,
                'total_enrollments': total_enrollments,
                'total_certificates': total_certificates,
                'total_attempts': total_attempts,
                'pass_rate': pass_rate,
                'completion_rate': completion_rate
            },
            'top_courses': list(top_courses),
            'recent_enrollments': recent_activity_data,
            'recent_certificates': recent_certs_data
        })
