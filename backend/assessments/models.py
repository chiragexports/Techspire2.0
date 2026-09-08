from django.db import models
from django.conf import settings
from courses.models import Course

class Assessment(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='assessment')
    title = models.CharField(max_length=200)
    description = models.TextField()
    passing_score = models.IntegerField(default=70, help_text="Passing percentage (e.g., 70 for 70%)")
    time_limit_minutes = models.IntegerField(default=25)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Assessment: {self.course.title} - {self.title}"

    @property
    def total_questions(self):
        return self.questions.count()

    @property
    def total_points(self):
        return sum(q.points for q in self.questions.all())

class Question(models.Model):
    QUESTION_TYPES = (
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Choice'),
        ('code', 'Code Analysis'),
    )

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='single')
    code_context = models.TextField(blank=True, null=True)
    code_language = models.CharField(max_length=30, default='python')
    explanation = models.TextField(help_text="Explanation revealed only after test completion.")
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:60]}..."

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.question.id} -> {self.option_text[:40]}"

class AssessmentAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    passed = models.BooleanField(default=False)
    time_spent_seconds = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at', '-started_at']

    def __str__(self):
        status = "PASSED" if self.passed else "FAILED"
        return f"{self.user.email} -> {self.assessment.title}: {self.percentage}% ({status})"

class AssessmentAnswer(models.Model):
    attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.CASCADE, blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        unique_together = ('attempt', 'question')
