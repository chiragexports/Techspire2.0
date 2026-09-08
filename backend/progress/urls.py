from django.urls import path
from .views import (
    EnrollCourseView, MyCoursesListView, MarkChapterProgressView,
    CourseProgressStatusView, StudentDashboardOverviewView
)

urlpatterns = [
    path('courses/<str:course_id_or_slug>/enroll/', EnrollCourseView.as_view(), name='enroll_course'),
    path('my-courses/', MyCoursesListView.as_view(), name='my_courses'),
    path('progress/mark-chapter/', MarkChapterProgressView.as_view(), name='mark_chapter_progress'),
    path('progress/course/<slug:course_slug>/', CourseProgressStatusView.as_view(), name='course_progress_status'),
    path('dashboard/overview/', StudentDashboardOverviewView.as_view(), name='dashboard_overview'),
]
