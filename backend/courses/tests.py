from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Category, Course, Module, Chapter
from assessments.models import Assessment, Question, QuestionOption, AssessmentAttempt
from certificates.models import Certificate

User = get_user_model()

class TechspireBackendTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = User.objects.create_user(
            email='teststudent@techspire.io',
            username='teststudent',
            password='TestPassword123!',
            role='student'
        )

        self.category = Category.objects.create(name='Languages', slug='languages')
        self.course = Course.objects.create(
            title='Python Fundamentals',
            slug='python-fundamentals',
            tagline='Learn Python fast',
            description='Test course description',
            category=self.category,
            difficulty='beginner',
            estimated_hours=10,
            is_free=True,
            price_in_paise=0
        )
        self.module = Module.objects.create(course=self.course, title='Module 1', order=1)
        self.chapter1 = Chapter.objects.create(
            module=self.module,
            title='Chapter 1: Intro',
            slug='chapter-1-intro',
            order=1,
            content_markdown='# Intro Chapter\nWelcome to Python.'
        )
        self.chapter2 = Chapter.objects.create(
            module=self.module,
            title='Chapter 2: Data Types',
            slug='chapter-2-datatypes',
            order=2,
            content_markdown='# Data Types\nLearn lists and dicts.'
        )

        # Assessment
        self.assessment = Assessment.objects.create(
            course=self.course,
            title='Python Quiz',
            description='Test quiz',
            passing_score=70
        )
        self.question = Question.objects.create(
            assessment=self.assessment,
            question_text='Is Python awesome?',
            explanation='Yes, Python is awesome.',
            points=100
        )
        self.opt_correct = QuestionOption.objects.create(
            question=self.question,
            option_text='Yes, absolutely',
            is_correct=True
        )
        self.opt_wrong = QuestionOption.objects.create(
            question=self.question,
            option_text='No',
            is_correct=False
        )

    def test_user_authentication_flow(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'teststudent@techspire.io',
            'password': 'TestPassword123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        token = response.data['tokens']['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        profile_res = self.client.get('/api/auth/me/')
        self.assertEqual(profile_res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_res.data['email'], 'teststudent@techspire.io')

    def test_course_flow_and_progress_tracking(self):
        # Authenticate
        self.client.force_authenticate(user=self.student)

        # 1. Enroll
        enroll_res = self.client.post(f'/api/courses/{self.course.slug}/enroll/')
        self.assertEqual(enroll_res.status_code, status.HTTP_201_CREATED)

        # 2. Mark chapter 1 as completed
        progress_res = self.client.post('/api/progress/mark-chapter/', {
            'chapter_id': self.chapter1.id,
            'is_completed': True
        })
        self.assertEqual(progress_res.status_code, status.HTTP_200_OK)
        self.assertEqual(progress_res.data['course_progress_percentage'], 50)

        # 3. Mark chapter 2 as completed
        progress_res2 = self.client.post('/api/progress/mark-chapter/', {
            'chapter_id': self.chapter2.id,
            'is_completed': True
        })
        self.assertEqual(progress_res2.status_code, status.HTTP_200_OK)
        self.assertEqual(progress_res2.data['course_progress_percentage'], 100)
        self.assertTrue(progress_res2.data['is_course_completed'])

    def test_assessment_submission_and_certificate_issuance(self):
        self.client.force_authenticate(user=self.student)

        # Submit passing answers
        submit_res = self.client.post(f'/api/assessments/{self.assessment.id}/submit/', {
            'answers': {
                str(self.question.id): self.opt_correct.id
            },
            'time_spent_seconds': 120
        }, format='json')
        self.assertEqual(submit_res.status_code, status.HTTP_200_OK)
        self.assertTrue(submit_res.data['passed'])
        self.assertEqual(submit_res.data['percentage'], 100.0)
        self.assertIsNotNone(submit_res.data['certificate_code'])

        cert_code = submit_res.data['certificate_code']

        # Verify certificate on public endpoint without auth
        public_client = APIClient()
        verify_res = public_client.get(f'/api/certificates/verify/{cert_code}/')
        self.assertEqual(verify_res.status_code, status.HTTP_200_OK)
        self.assertTrue(verify_res.data['is_valid'])
        self.assertEqual(verify_res.data['certificate']['course_title'], 'Python Fundamentals')
