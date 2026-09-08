from django.db import models
from django.conf import settings

class PlatformAuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.email if self.user else "Anonymous"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {user_str}: {self.action}"
