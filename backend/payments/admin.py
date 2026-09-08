from django.contrib import admin
from .models import PaymentOrder, Payment, WebhookEvent

@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ('razorpay_order_id', 'user', 'course', 'amount_in_rupees', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'course')
    search_fields = ('razorpay_order_id', 'user__email', 'course__title')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('razorpay_payment_id', 'user', 'course', 'amount_in_rupees', 'status', 'method', 'created_at')
    list_filter = ('status', 'method', 'created_at', 'course')
    search_fields = ('razorpay_payment_id', 'user__email', 'course__title', 'payment_order__razorpay_order_id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'event_type', 'processed', 'created_at')
    list_filter = ('event_type', 'processed', 'created_at')
    search_fields = ('event_id', 'event_type')
