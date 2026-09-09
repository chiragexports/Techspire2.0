from django.urls import path
from .views import AdminAnalyticsOverviewView

urlpatterns = [
    path('admin/analytics/overview/', AdminAnalyticsOverviewView.as_view(), name='admin_analytics_overview'),
    path('admin/analytics/overview', AdminAnalyticsOverviewView.as_view(), name='admin_analytics_overview_noslash'),
]
