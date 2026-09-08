import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techspire_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Course
from assessments.models import Assessment, AssessmentAttempt, AssessmentAnswer
from progress.models import Enrollment, CourseProgress, ChapterProgress
from progress.services import CourseCompletionService
from certificates.models import Certificate

User = get_user_model()
student = User.objects.get(email='student@techspire.io')
course = Course.objects.get(slug='python-programming')

print("Student:", student.email)
print("Course:", course.title, f"({course.total_chapters} chapters)")

# Check initial progress
prog = CourseCompletionService.recalculate_course_progress(student, course)
print(f"Initial progress: {prog.percentage}% ({prog.completed_chapters_count}/{prog.total_chapters_count})")

# Submit assessment with passing score (100%)
assessment = Assessment.objects.filter(course=course).first()
if assessment:
    print(f"Found assessment: {assessment.title}")
    questions = list(assessment.questions.all())
    total_pts = sum(q.points for q in questions)
    attempt = AssessmentAttempt.objects.create(
        user=student,
        assessment=assessment,
        score=total_pts,
        total_points=total_pts,
        percentage=100.0,
        passed=True,
        time_spent_seconds=120
    )
    for q in questions:
        opt = q.options.filter(is_correct=True).first()
        AssessmentAnswer.objects.create(
            attempt=attempt,
            question=q,
            selected_option=opt,
            is_correct=True
        )
    
    course_prog, cert = CourseCompletionService.record_assessment_submission(
        user=student,
        assessment=assessment,
        attempt=attempt,
        percentage=100.0,
        passed=True
    )
    
    print("\n=== POST ASSESSMENT SUBMISSION ===")
    print(f"Course Completed: {course_prog.is_completed}")
    print(f"Progress Percentage: {course_prog.percentage}%")
    print(f"Certificate Code: {cert.certificate_code}")
    print(f"Certificate ID: {cert.id}")
    print(f"Verify URL: /verify/{cert.certificate_code}")
    print(f"Print URL: /certificates/{cert.id}/print")
