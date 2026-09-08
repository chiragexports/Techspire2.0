from rest_framework import serializers
from .models import Enrollment, ChapterProgress
from courses.models import Course, Chapter
from courses.serializers import CourseListSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    completed_chapters_count = serializers.SerializerMethodField()
    total_chapters_count = serializers.SerializerMethodField()
    next_up_chapter = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'course', 'status', 'enrolled_at', 'completed_at',
            'last_accessed_at', 'progress_percentage', 'completed_chapters_count',
            'total_chapters_count', 'next_up_chapter'
        ]

    def get_progress_percentage(self, obj):
        return obj.calculate_progress()

    def get_completed_chapters_count(self, obj):
        return ChapterProgress.objects.filter(
            user=obj.user,
            chapter__module__course=obj.course,
            is_completed=True
        ).count()

    def get_total_chapters_count(self, obj):
        return obj.course.total_chapters

    def get_next_up_chapter(self, obj):
        completed_ids = ChapterProgress.objects.filter(
            user=obj.user,
            chapter__module__course=obj.course,
            is_completed=True
        ).values_list('chapter_id', flat=True)

        # Find first chapter in course that is NOT completed
        next_ch = Chapter.objects.filter(
            module__course=obj.course
        ).exclude(id__in=completed_ids).order_by('module__order', 'order').first()

        if not next_ch:
            # Fallback to first chapter
            next_ch = Chapter.objects.filter(module__course=obj.course).order_by('module__order', 'order').first()

        if next_ch:
            return {
                'id': next_ch.id,
                'title': next_ch.title,
                'slug': next_ch.slug,
                'module_title': next_ch.module.title,
            }
        return None

class ChapterProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterProgress
        fields = ['id', 'chapter', 'is_completed', 'completed_at', 'last_accessed_at', 'notes_bookmarked']
