from django.db import models
from django.conf import settings
from courses.models import Course
import uuid

class PaymentOrder(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('attempted', 'Attempted'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_orders')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payment_orders')
    razorpay_order_id = models.CharField(max_length=100, unique=True, db_index=True)
    amount = models.IntegerField(help_text="Amount in paise (e.g. 149900 for ₹1,499)")
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', db_index=True)
    receipt = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.razorpay_order_id} ({self.user.email} -> {self.course.title} - ₹{self.amount // 100}) [{self.status}]"

    @property
    def amount_in_rupees(self):
        return self.amount // 100 if self.amount else 0

class Payment(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('authorized', 'Authorized'),
        ('captured', 'Captured'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_order = models.ForeignKey(PaymentOrder, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    razorpay_payment_id = models.CharField(max_length=100, unique=True, db_index=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    amount = models.IntegerField(help_text="Captured amount in paise")
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='captured', db_index=True)
    method = models.CharField(max_length=50, blank=True, null=True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    wallet = models.CharField(max_length=50, blank=True, null=True)
    vpa = models.CharField(max_length=100, blank=True, null=True)
    error_code = models.CharField(max_length=100, blank=True, null=True)
    error_description = models.TextField(blank=True, null=True)
    captured_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.razorpay_payment_id} (₹{self.amount // 100}) [{self.status}]"

    @property
    def amount_in_rupees(self):
        return self.amount // 100 if self.amount else 0

class WebhookEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.CharField(max_length=100, unique=True, db_index=True)
    event_type = models.CharField(max_length=100, db_index=True)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Webhook {self.event_type} - {self.event_id}"
