import uuid
import hashlib
from django.db import models
from django.conf import settings
from courses.models import Course
from assessments.models import AssessmentAttempt

def generate_cert_code():
    random_part = uuid.uuid4().hex[:8].upper()
    return f"TECHSPIRE-2026-{random_part}"

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    certificate_code = models.CharField(max_length=64, unique=True, default=generate_cert_code)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.SET_NULL, null=True, blank=True)
    grade_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    issue_date = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    verification_hash = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-issue_date']

    def save(self, *args, **kwargs):
        if not self.verification_hash:
            raw = f"{self.user_id}:{self.course_id}:{self.certificate_code}:techspire-secret-hash"
            self.verification_hash = hashlib.sha256(raw.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.certificate_code} -> {self.user.email} ({self.course.title})"
