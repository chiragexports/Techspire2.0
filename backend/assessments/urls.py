from django.urls import path
from .views import (
    CourseAssessmentDetailView, SubmitAssessmentView, AssessmentAttemptHistoryView,
    AssessmentAttemptDetailView, AdminAssessmentListCreateView, AdminAssessmentDetailView,
    AdminQuestionCreateView, AdminQuestionDetailView
)

urlpatterns = [
    # Student Endpoints
    path('assessments/course/<slug:course_slug>/', CourseAssessmentDetailView.as_view(), name='course_assessment'),
    path('assessments/course/<slug:course_slug>', CourseAssessmentDetailView.as_view(), name='course_assessment_noslash'),
    path('assessments/<int:assessment_id>/submit/', SubmitAssessmentView.as_view(), name='submit_assessment'),
    path('assessments/<int:assessment_id>/submit', SubmitAssessmentView.as_view(), name='submit_assessment_noslash'),
    path('assessments/attempts/', AssessmentAttemptHistoryView.as_view(), name='assessment_attempts'),
    path('assessments/attempts', AssessmentAttemptHistoryView.as_view(), name='assessment_attempts_noslash'),
    path('assessments/attempts/<int:pk>/', AssessmentAttemptDetailView.as_view(), name='assessment_attempt_detail'),
    path('assessments/attempts/<int:pk>', AssessmentAttemptDetailView.as_view(), name='assessment_attempt_detail_noslash'),

    # Admin Endpoints
    path('admin/assessments/', AdminAssessmentListCreateView.as_view(), name='admin_assessments'),
    path('admin/assessments', AdminAssessmentListCreateView.as_view(), name='admin_assessments_noslash'),
    path('admin/assessments/<int:pk>/', AdminAssessmentDetailView.as_view(), name='admin_assessment_detail'),
    path('admin/assessments/<int:pk>', AdminAssessmentDetailView.as_view(), name='admin_assessment_detail_noslash'),
    path('admin/questions/', AdminQuestionCreateView.as_view(), name='admin_questions_create'),
    path('admin/questions', AdminQuestionCreateView.as_view(), name='admin_questions_create_noslash'),
    path('admin/questions/<int:pk>/', AdminQuestionDetailView.as_view(), name='admin_question_detail'),
    path('admin/questions/<int:pk>', AdminQuestionDetailView.as_view(), name='admin_question_detail_noslash'),
]
