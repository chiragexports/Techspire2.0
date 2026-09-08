from django.urls import path
from .views import (
    CreatePaymentOrderView,
    VerifyPaymentView,
    RazorpayWebhookView,
    StudentPaymentHistoryView,
    AdminPaymentListView,
    AdminPaymentStatsView
)

urlpatterns = [
    path('create-order/', CreatePaymentOrderView.as_view(), name='create_order'),
    path('verify/', VerifyPaymentView.as_view(), name='verify_payment'),
    path('webhook/', RazorpayWebhookView.as_view(), name='razorpay_webhook'),
    path('history/', StudentPaymentHistoryView.as_view(), name='payment_history'),
    path('admin/list/', AdminPaymentListView.as_view(), name='admin_payment_list'),
    path('admin/stats/', AdminPaymentStatsView.as_view(), name='admin_payment_stats'),
]
