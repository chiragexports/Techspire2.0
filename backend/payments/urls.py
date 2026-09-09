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
    path('create-order', CreatePaymentOrderView.as_view(), name='create_order_noslash'),
    path('verify/', VerifyPaymentView.as_view(), name='verify_payment'),
    path('verify', VerifyPaymentView.as_view(), name='verify_payment_noslash'),
    path('webhook/', RazorpayWebhookView.as_view(), name='razorpay_webhook'),
    path('webhook', RazorpayWebhookView.as_view(), name='razorpay_webhook_noslash'),
    path('history/', StudentPaymentHistoryView.as_view(), name='payment_history'),
    path('history', StudentPaymentHistoryView.as_view(), name='payment_history_noslash'),
    path('admin/list/', AdminPaymentListView.as_view(), name='admin_payment_list'),
    path('admin/list', AdminPaymentListView.as_view(), name='admin_payment_list_noslash'),
    path('admin/stats/', AdminPaymentStatsView.as_view(), name='admin_payment_stats'),
    path('admin/stats', AdminPaymentStatsView.as_view(), name='admin_payment_stats_noslash'),
]
