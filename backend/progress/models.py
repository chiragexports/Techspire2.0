from django.db import models
from django.conf import settings
from courses.models import Course, Module, Chapter

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    paid = models.BooleanField(default=True)
    purchase_price_in_paise = models.IntegerField(default=0, help_text="Amount paid in paise at enrollment")
    payment = models.ForeignKey('payments.Payment', on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_accessed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-last_accessed_at']

    def __str__(self):
        return f"{self.user.email} -> {self.course.title} ({self.status})"

    def calculate_progress(self):
        from progress.services import CourseCompletionService
        progress_obj = CourseCompletionService.get_or_create_course_progress(self.user, self.course)
        return progress_obj.percentage

class ChapterProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chapter_progress')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_accessed_at = models.DateTimeField(auto_now=True)
    notes_bookmarked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'chapter')
        ordering = ['-last_accessed_at']

    def __str__(self):
        status = "Done" if self.is_completed else "In Progress"
        return f"{self.user.email} -> {self.chapter.title} [{status}]"

class ModuleProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    completed_chapters_count = models.IntegerField(default=0)
    total_chapters_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'module')

    def __str__(self):
        return f"{self.user.email} -> {self.module.title} ({self.completed_chapters_count}/{self.total_chapters_count})"

class CourseProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_progress')
    percentage = models.IntegerField(default=0)
    completed_chapters_count = models.IntegerField(default=0)
    total_chapters_count = models.IntegerField(default=0)
    final_assessment_passed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-last_updated_at']

    def __str__(self):
        status = "COMPLETED" if self.is_completed else f"{self.percentage}%"
        return f"{self.user.email} -> {self.course.title} [{status}]"
