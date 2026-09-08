from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from courses.models import Category, Course, Module, Chapter
from assessments.models import Assessment, Question, QuestionOption, AssessmentAttempt, AssessmentAnswer
from progress.models import Enrollment, ChapterProgress
from certificates.models import Certificate
from courses_content_data import COURSES_DATA

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with 9 complete, high-quality technical courses, users, and assessments'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Techspire production curricula..."))

        # Create Admin User
        admin_user, created = User.objects.get_or_create(
            email='admin@techspire.io',
            defaults={
                'username': 'techspire_admin',
                'first_name': 'Chief',
                'last_name': 'Architect',
                'role': 'admin',
                'headline': 'Techspire System Administrator & Principal Lead',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123456')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin@techspire.io / admin123456"))

        # Create Student User
        student_user, created = User.objects.get_or_create(
            email='student@techspire.io',
            defaults={
                'username': 'alex_coder',
                'first_name': 'Alex',
                'last_name': 'Rivera',
                'role': 'student',
                'headline': 'Full-Stack Software Engineer In-Training'
            }
        )
        if created:
            student_user.set_password('student123456')
            student_user.save()
            self.stdout.write(self.style.SUCCESS("Created student user: student@techspire.io / student123456"))

        # Seed categories and courses
        for course_data in COURSES_DATA:
            cat_name = course_data.get('category', 'Computer Science')
            category, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    'slug': slugify(cat_name),
                    'icon': course_data.get('category_icon', 'Layers'),
                    'description': f'Core curriculum for {cat_name}'
                }
            )

            course, _ = Course.objects.update_or_create(
                slug=course_data['slug'],
                defaults={
                    'title': course_data['title'],
                    'tagline': course_data.get('tagline', course_data.get('description', '')[:200]),
                    'description': course_data.get('description', ''),
                    'category': category,
                    'difficulty': course_data.get('difficulty', course_data.get('level', 'intermediate')),
                    'estimated_hours': course_data.get('estimated_hours', course_data.get('duration_weeks', 8) * 4),
                    'badge_icon': course_data.get('badge_icon', 'Award'),
                    'color_accent': course_data.get('color_accent', '#38BDF8'),
                    'order': course_data.get('order', 1),
                    'prerequisites': course_data.get('prerequisites', []),
                    'learning_outcomes': course_data.get('learning_outcomes', []),
                    'is_published': True
                }
            )

            # Modules and Chapters
            for mod_idx, mod_data in enumerate(course_data['modules'], 1):
                module, _ = Module.objects.update_or_create(
                    course=course,
                    order=mod_idx,
                    defaults={
                        'title': mod_data['title'],
                        'description': mod_data.get('description', '')
                    }
                )

                for ch_idx, ch_data in enumerate(mod_data['chapters'], 1):
                    chapter_slug = slugify(f"{ch_data['title']}-{mod_idx}-{ch_idx}")
                    content = ch_data.get('content_markdown', ch_data.get('content', ''))
                    Chapter.objects.update_or_create(
                        module=module,
                        order=ch_idx,
                        defaults={
                            'title': ch_data['title'],
                            'slug': chapter_slug,
                            'duration_minutes': ch_data.get('duration_minutes', 20),
                            'is_free_preview': ch_data.get('is_free_preview', ch_idx == 1),
                            'content_markdown': content,
                            'code_snippet': ch_data.get('code_snippet', ''),
                            'code_language': ch_data.get('code_language', 'text'),
                            'key_takeaways': ch_data.get('key_takeaways', []),
                            'practice_questions': ch_data.get('practice_questions', [])
                        }
                    )

            # Seed Assessment
            if 'assessment' in course_data:
                ass_data = course_data['assessment']
                assessment, _ = Assessment.objects.update_or_create(
                    course=course,
                    defaults={
                        'title': ass_data['title'],
                        'description': ass_data['description'],
                        'passing_score': ass_data.get('passing_score', 70),
                        'time_limit_minutes': ass_data.get('time_limit_minutes', 20),
                        'is_published': True
                    }
                )

                # Remove old questions if re-seeding to keep clean
                assessment.questions.all().delete()

                for q_idx, q_data in enumerate(ass_data['questions'], 1):
                    question = Question.objects.create(
                        assessment=assessment,
                        question_text=q_data['question_text'],
                        question_type=q_data.get('question_type', 'single'),
                        code_context=q_data.get('code_context', ''),
                        code_language=q_data.get('code_language', 'python'),
                        explanation=q_data['explanation'],
                        points=q_data.get('points', 10),
                        order=q_idx
                    )

                    for opt_idx, opt_data in enumerate(q_data['options'], 1):
                        QuestionOption.objects.create(
                            question=question,
                            option_text=opt_data['text'],
                            is_correct=opt_data['is_correct'],
                            order=opt_idx
                        )

            self.stdout.write(self.style.SUCCESS(f"Loaded Course: {course.title} ({course.total_chapters} chapters)"))

        # Seed initial demo enrollment and progress for demo student
        py_course = Course.objects.get(slug='python-programming')
        enrollment, _ = Enrollment.objects.get_or_create(user=student_user, course=py_course)
        
        # Mark first 3 chapters of Python complete
        py_chapters = Chapter.objects.filter(module__course=py_course).order_by('module__order', 'order')[:3]
        for ch in py_chapters:
            ChapterProgress.objects.get_or_create(user=student_user, chapter=ch, defaults={'is_completed': True})
        
        enrollment.save()

        self.stdout.write(self.style.SUCCESS("Successfully completed Techspire seed!"))
