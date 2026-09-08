from django.urls import path
from .views import (
    CategoryListView, CourseListView, CourseDetailView, ChapterDetailView,
    AdminCourseListCreateView, AdminCourseDetailView,
    AdminModuleListCreateView, AdminModuleDetailView,
    AdminChapterListCreateView, AdminChapterDetailView
)

urlpatterns = [
    # Public Endpoints
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<slug:course_slug>/chapters/<slug:chapter_slug>/', ChapterDetailView.as_view(), name='chapter_detail'),

    # Admin Management Endpoints
    path('admin/courses/', AdminCourseListCreateView.as_view(), name='admin_courses'),
    path('admin/courses/<int:pk>/', AdminCourseDetailView.as_view(), name='admin_course_detail'),
    path('admin/modules/', AdminModuleListCreateView.as_view(), name='admin_modules'),
    path('admin/modules/<int:pk>/', AdminModuleDetailView.as_view(), name='admin_module_detail'),
    path('admin/chapters/', AdminChapterListCreateView.as_view(), name='admin_chapters'),
    path('admin/chapters/<int:pk>/', AdminChapterDetailView.as_view(), name='admin_chapter_detail'),
]
