from django.utils import timezone
from courses.models import Course, Module, Chapter
from progress.models import Enrollment, ChapterProgress, ModuleProgress, CourseProgress
from certificates.models import Certificate

class CourseCompletionService:
    @classmethod
    def get_or_create_course_progress(cls, user, course):
        progress, _ = CourseProgress.objects.get_or_create(
            user=user,
            course=course,
            defaults={
                'total_chapters_count': course.total_chapters,
                'percentage': 0,
                'completed_chapters_count': 0,
                'is_completed': False
            }
        )
        return cls.recalculate_course_progress(user, course, progress)

    @classmethod
    def recalculate_course_progress(cls, user, course, progress_obj=None):
        if not progress_obj:
            progress_obj, _ = CourseProgress.objects.get_or_create(user=user, course=course)

        total_chapters = course.total_chapters
        progress_obj.total_chapters_count = total_chapters

        # Count completed chapters for this user in this course
        completed_chapters = ChapterProgress.objects.filter(
            user=user,
            chapter__module__course=course,
            is_completed=True
        ).count()

        progress_obj.completed_chapters_count = completed_chapters

        # Check if user has passed assessment or has valid certificate
        has_cert = Certificate.objects.filter(user=user, course=course, is_valid=True).exists()
        if has_cert:
            progress_obj.final_assessment_passed = True

        # Calculate percentage deterministically
        if total_chapters > 0:
            pct = round((completed_chapters / total_chapters) * 100)
        else:
            pct = 100 if progress_obj.final_assessment_passed else 0

        # If user has earned certificate or passed assessment with >= 90% chapters or 100%
        if progress_obj.final_assessment_passed and (pct >= 90 or completed_chapters == total_chapters):
            pct = 100

        # If 100% completed or certificate exists, mark as complete
        if pct >= 100 or (has_cert and completed_chapters == total_chapters):
            pct = 100
            progress_obj.is_completed = True
            if not progress_obj.completed_at:
                progress_obj.completed_at = timezone.now()
        else:
            progress_obj.is_completed = False

        progress_obj.percentage = pct
        progress_obj.save()

        # Synchronize Enrollment
        enrollment, _ = Enrollment.objects.get_or_create(
            user=user,
            course=course,
            defaults={'status': 'completed' if progress_obj.is_completed else 'active'}
        )
        if progress_obj.is_completed:
            enrollment.status = 'completed'
            if not enrollment.completed_at:
                enrollment.completed_at = progress_obj.completed_at or timezone.now()
        else:
            enrollment.status = 'active'
        enrollment.last_accessed_at = timezone.now()
        enrollment.save()

        return progress_obj

    @classmethod
    def mark_chapter(cls, user, chapter, is_completed=True):
        course = chapter.module.course

        # 1. Update ChapterProgress
        ch_prog, _ = ChapterProgress.objects.get_or_create(user=user, chapter=chapter)
        ch_prog.is_completed = is_completed
        ch_prog.completed_at = timezone.now() if is_completed else None
        ch_prog.save()

        # 2. Update ModuleProgress
        module = chapter.module
        mod_total = module.chapters.count()
        mod_completed = ChapterProgress.objects.filter(
            user=user,
            chapter__module=module,
            is_completed=True
        ).count()

        mod_prog, _ = ModuleProgress.objects.get_or_create(
            user=user,
            module=module,
            defaults={'total_chapters_count': mod_total}
        )
        mod_prog.total_chapters_count = mod_total
        mod_prog.completed_chapters_count = mod_completed
        mod_prog.is_completed = (mod_completed == mod_total and mod_total > 0)
        if mod_prog.is_completed and not mod_prog.completed_at:
            mod_prog.completed_at = timezone.now()
        mod_prog.save()

        # 3. Recalculate CourseProgress
        course_prog = cls.recalculate_course_progress(user, course)

        return course_prog

    @classmethod
    def record_assessment_submission(cls, user, assessment, attempt, percentage, passed):
        course = assessment.course
        cert_obj = None

        if passed:
            # Issue or update certificate
            cert_obj, created = Certificate.objects.get_or_create(
                user=user,
                course=course,
                defaults={
                    'attempt': attempt,
                    'grade_percentage': percentage,
                    'is_valid': True
                }
            )
            if not created and percentage > cert_obj.grade_percentage:
                cert_obj.grade_percentage = percentage
                cert_obj.attempt = attempt
                cert_obj.save()

            # Mark all course chapters as completed if student passed final comprehensive exam
            # This ensures complete synchronization between exam pass and curriculum checkmarks!
            all_chapters = Chapter.objects.filter(module__course=course)
            for ch in all_chapters:
                ChapterProgress.objects.update_or_create(
                    user=user,
                    chapter=ch,
                    defaults={'is_completed': True, 'completed_at': timezone.now()}
                )

        # Recalculate course progress
        course_prog = cls.recalculate_course_progress(user, course)

        return course_prog, cert_obj
