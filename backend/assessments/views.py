from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Assessment, Question, QuestionOption, AssessmentAttempt, AssessmentAnswer
from .serializers import (
    StudentAssessmentSerializer, AssessmentAttemptDetailSerializer,
    AdminAssessmentSerializer, AdminQuestionSerializer, AdminOptionSerializer
)
from courses.models import Course
from certificates.models import Certificate
from accounts.permissions import IsTechspireAdmin

class CourseAssessmentDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, course_slug):
        try:
            course = Course.objects.get(slug=course_slug, is_published=True)
            assessment = Assessment.objects.select_related('course').prefetch_related('questions__options').get(
                course=course,
                is_published=True
            )
        except (Course.DoesNotExist, Assessment.DoesNotExist):
            return Response({'error': 'Assessment not found for this course.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentAssessmentSerializer(assessment)
        return Response(serializer.data)

class SubmitAssessmentView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, assessment_id):
        try:
            assessment = Assessment.objects.select_related('course').prefetch_related('questions__options').get(
                id=assessment_id,
                is_published=True
            )
        except Assessment.DoesNotExist:
            return Response({'error': 'Assessment not found.'}, status=status.HTTP_404_NOT_FOUND)

        answers_payload = request.data.get('answers', {}) # Dict of {question_id: option_id}
        time_spent = int(request.data.get('time_spent_seconds', 0))

        questions = assessment.questions.all()
        total_points = sum(q.points for q in questions)
        earned_points = 0

        attempt = AssessmentAttempt.objects.create(
            user=request.user,
            assessment=assessment,
            total_points=total_points,
            time_spent_seconds=time_spent,
            submitted_at=timezone.now()
        )

        for question in questions:
            chosen_opt_id = answers_payload.get(str(question.id)) or answers_payload.get(question.id)
            selected_option = None
            is_correct = False

            if chosen_opt_id:
                selected_option = question.options.filter(id=chosen_opt_id).first()
                if selected_option and selected_option.is_correct:
                    is_correct = True
                    earned_points += question.points

            AssessmentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

        percentage = round((earned_points / total_points * 100), 2) if total_points > 0 else 0
        passed = percentage >= assessment.passing_score

        attempt.score = earned_points
        attempt.percentage = percentage
        attempt.passed = passed
        attempt.save()

        # Synchronize course completion and issue certificate via CourseCompletionService
        from progress.services import CourseCompletionService
        course_prog, certificate_obj = CourseCompletionService.record_assessment_submission(
            user=request.user,
            assessment=assessment,
            attempt=attempt,
            percentage=percentage,
            passed=passed
        )

        attempt_serializer = AssessmentAttemptDetailSerializer(attempt)
        
        return Response({
            'success': True,
            'passed': passed,
            'score': earned_points,
            'total_points': total_points,
            'percentage': percentage,
            'passing_score': assessment.passing_score,
            'certificate_code': certificate_obj.certificate_code if certificate_obj else None,
            'certificate_id': str(certificate_obj.id) if certificate_obj else None,
            'course_progress_percentage': course_prog.percentage,
            'is_course_completed': course_prog.is_completed,
            'attempt': attempt_serializer.data
        }, status=status.HTTP_200_OK)

class AssessmentAttemptHistoryView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssessmentAttemptDetailSerializer

    def get_queryset(self):
        return AssessmentAttempt.objects.filter(user=self.request.user).select_related('assessment', 'assessment__course')

class AssessmentAttemptDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AssessmentAttemptDetailSerializer

    def get_queryset(self):
        return AssessmentAttempt.objects.filter(user=self.request.user).select_related('assessment', 'assessment__course')

# Admin Assessment CRUD Views
class AdminAssessmentListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Assessment.objects.all().order_by('-id')
    serializer_class = AdminAssessmentSerializer

class AdminAssessmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Assessment.objects.all()
    serializer_class = AdminAssessmentSerializer

class AdminQuestionCreateView(generics.CreateAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Question.objects.all()
    serializer_class = AdminQuestionSerializer

class AdminQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Question.objects.all()
    serializer_class = AdminQuestionSerializer
