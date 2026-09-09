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
from django.db import connection
from django.core.management import call_command

logger = logging.getLogger(__name__)

SLUG_ALIASES = {
    'sql-databases': 'master-sql-relational-database-architecture',
    'data-structures': 'data-structures-algorithms-depth',
    'oop-design-patterns': 'object-oriented-design-patterns',
    'ai-fundamentals': 'artificial-intelligence-modern-llm-engineering',
    'machine-learning': 'machine-learning-engineering-mlops-production',
    'operating-systems': 'operating-systems-low-level-architecture',
}

def resolve_course_slug(slug: str) -> str:
    """Resolve a given slug to its canonical version if aliased."""
    return SLUG_ALIASES.get(slug, slug)

def ensure_database_ready():
    """Ensure database tables are migrated and the 9 flagship curricula are seeded."""
    try:
        table_names = connection.introspection.table_names()
        if 'courses_course' not in table_names or 'accounts_user' not in table_names:
            logger.info("Core database tables missing. Running Django migrations...")
            call_command('migrate', interactive=False)

        if Course.objects.filter(is_published=True).count() == 0:
            logger.info("Empty course catalog detected. Triggering seed_techspire...")
            call_command('seed_techspire')
    except Exception as e:
        logger.error(f"Error while verifying/initializing database: {e}", exc_info=True)

class CategoryListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        ensure_database_ready()
        return Category.objects.all()

class CourseListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CourseListSerializer

    def get_queryset(self):
        ensure_database_ready()
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

    def get_object(self):
        ensure_database_ready()
        raw_slug = self.kwargs.get('slug', '')
        resolved_slug = resolve_course_slug(raw_slug)

        # Check resolved slug or raw slug or reverse alias
        course = Course.objects.filter(
            Q(slug=resolved_slug) | Q(slug=raw_slug),
            is_published=True
        ).first()

        if not course:
            # Check if any course slug ends with or matches
            for alias, canonical in SLUG_ALIASES.items():
                if raw_slug in (alias, canonical):
                    course = Course.objects.filter(Q(slug=canonical) | Q(slug=alias), is_published=True).first()
                    if course:
                        break

        if not course:
            from rest_framework.exceptions import NotFound
            raise NotFound(detail=f"Course '{raw_slug}' not found.")

        self.check_object_permissions(self.request, course)
        return course

class ChapterDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, course_slug, chapter_slug):
        ensure_database_ready()
        resolved_course_slug = resolve_course_slug(course_slug)

        course = Course.objects.filter(
            Q(slug=resolved_course_slug) | Q(slug=course_slug),
            is_published=True
        ).first()

        if not course:
            return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

        chapter = Chapter.objects.select_related('module__course').filter(
            module__course=course,
            slug=chapter_slug
        ).first()

        if not chapter:
            return Response({'error': 'Chapter not found.'}, status=status.HTTP_404_NOT_FOUND)

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
