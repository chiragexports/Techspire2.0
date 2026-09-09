from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, UserProfileView, AdminUserListView, AdminUserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('register', RegisterView.as_view(), name='auth_register_noslash'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('login', LoginView.as_view(), name='auth_login_noslash'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('refresh', TokenRefreshView.as_view(), name='auth_refresh_noslash'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
    path('me', UserProfileView.as_view(), name='user_profile_noslash'),
    path('admin/users/', AdminUserListView.as_view(), name='admin_users_list'),
    path('admin/users', AdminUserListView.as_view(), name='admin_users_list_noslash'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin/users/<int:pk>', AdminUserDetailView.as_view(), name='admin_user_detail_noslash'),
]
