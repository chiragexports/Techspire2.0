from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Category, Course, Module, Chapter
from .serializers import (
    CategorySerializer, CourseListSerializer, CourseDetailSerializer,
    ChapterDetailSerializer, AdminCourseSerializer, AdminModuleSerializer, AdminChapterSerializer
)
from accounts.permissions import IsAdminOrReadOnly, IsTechspireAdmin

import logging
logger = logging.getLogger(__name__)

def ensure_courses_seeded():
    """Ensure database has the 9 flagship curricula seeded."""
    try:
        if Course.objects.filter(is_published=True).count() == 0:
            from django.core.management import call_command
            logger.info("Empty course table detected. Triggering seed_techspire command...")
            call_command('seed_techspire')
    except Exception as e:
        logger.error(f"Error while auto-seeding courses: {e}")

class CategoryListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        ensure_courses_seeded()
        return Category.objects.all()

class CourseListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CourseListSerializer

    def get_queryset(self):
        ensure_courses_seeded()
        queryset = Course.objects.filter(is_published=True).select_related('category').prefetch_related('modules__chapters')
        
        search = self.request.query_params.get('search', '').strip()
        category = self.request.query_params.get('category', '').strip()
        difficulty = self.request.query_params.get('difficulty', '').strip()
        sort_by = self.request.query_params.get('sort', 'order').strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(tagline__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )
        if category:
            queryset = queryset.filter(category__slug=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        if sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'hours_asc':
            queryset = queryset.order_by('estimated_hours')
        elif sort_by == 'hours_desc':
            queryset = queryset.order_by('-estimated_hours')
        elif sort_by == 'title':
            queryset = queryset.order_by('title')
        else:
            queryset = queryset.order_by('order', 'id')

        return queryset

class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'
    queryset = Course.objects.filter(is_published=True)

class ChapterDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, course_slug, chapter_slug):
        try:
            course = Course.objects.get(slug=course_slug, is_published=True)
            chapter = Chapter.objects.select_related('module__course').get(
                module__course=course,
                slug=chapter_slug
            )
        except (Course.DoesNotExist, Chapter.DoesNotExist):
            return Response({'error': 'Chapter or Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Access Control Gating:
        # If lesson is free preview or entire course is free, allow.
        # Otherwise, user must be authenticated with an active paid enrollment (or staff/admin).
        if not course.is_free and not chapter.is_free_preview:
            is_authorized = False
            if request.user.is_authenticated:
                if request.user.is_staff or getattr(request.user, 'role', '') == 'admin':
                    is_authorized = True
                else:
                    from progress.models import Enrollment
                    is_authorized = Enrollment.objects.filter(
                        user=request.user,
                        course=course,
                        status='active',
                        paid=True
                    ).exists()

            if not is_authorized:
                return Response({
                    'error': 'Payment required to access this lesson.',
                    'code': 'payment_required',
                    'course_slug': course.slug,
                    'course_title': course.title,
                    'price_in_rupees': course.price_in_rupees,
                    'is_authenticated': request.user.is_authenticated
                }, status=status.HTTP_403_FORBIDDEN)

        serializer = ChapterDetailSerializer(chapter, context={'request': request})
        return Response(serializer.data)

# Admin CRUD Views
class AdminCourseListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Course.objects.all().order_by('order', 'id')
    serializer_class = AdminCourseSerializer

class AdminCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Course.objects.all()
    serializer_class = AdminCourseSerializer

class AdminModuleListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Module.objects.all().order_by('order', 'id')
    serializer_class = AdminModuleSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            qs = qs.filter(course_id=course_id)
        return qs

class AdminModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Module.objects.all()
    serializer_class = AdminModuleSerializer

class AdminChapterListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Chapter.objects.all().order_by('order', 'id')
    serializer_class = AdminChapterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        module_id = self.request.query_params.get('module_id')
        if module_id:
            qs = qs.filter(module_id=module_id)
        return qs

class AdminChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsTechspireAdmin,)
    queryset = Chapter.objects.all()
    serializer_class = AdminChapterSerializer
