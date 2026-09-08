from rest_framework import serializers
from .models import Assessment, Question, QuestionOption, AssessmentAttempt, AssessmentAnswer

# Public student option serializer (No is_correct field)
class StudentQuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'option_text', 'order']

# Public student question serializer (No explanation)
class StudentQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'code_context', 'code_language', 'points', 'order', 'options']

    def get_options(self, obj):
        options = obj.options.all().order_by('order')
        return StudentQuestionOptionSerializer(options, many=True).data

# Public student assessment serializer
class StudentAssessmentSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)

    class Meta:
        model = Assessment
        fields = [
            'id', 'title', 'description', 'passing_score', 'time_limit_minutes',
            'course_title', 'course_slug', 'total_questions', 'total_points', 'questions'
        ]

    def get_questions(self, obj):
        questions = obj.questions.all().order_by('order')
        return StudentQuestionSerializer(questions, many=True).data

# Post-submission detailed answer review serializer
class AnswerReviewSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    explanation = serializers.CharField(source='question.explanation', read_only=True)
    selected_option_id = serializers.IntegerField(source='selected_option.id', read_only=True)
    selected_option_text = serializers.CharField(source='selected_option.option_text', read_only=True)
    correct_option_id = serializers.SerializerMethodField()
    correct_option_text = serializers.SerializerMethodField()
    all_options = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentAnswer
        fields = [
            'id', 'question_text', 'explanation', 'selected_option_id',
            'selected_option_text', 'correct_option_id', 'correct_option_text',
            'is_correct', 'all_options'
        ]

    def get_correct_option_id(self, obj):
        correct = obj.question.options.filter(is_correct=True).first()
        return correct.id if correct else None

    def get_correct_option_text(self, obj):
        correct = obj.question.options.filter(is_correct=True).first()
        return correct.option_text if correct else ""

    def get_all_options(self, obj):
        return [
            {
                'id': opt.id,
                'option_text': opt.option_text,
                'is_correct': opt.is_correct
            }
            for opt in obj.question.options.all().order_by('order')
        ]

class AssessmentAttemptDetailSerializer(serializers.ModelSerializer):
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    course_title = serializers.CharField(source='assessment.course.title', read_only=True)
    course_slug = serializers.CharField(source='assessment.course.slug', read_only=True)
    passing_score = serializers.IntegerField(source='assessment.passing_score', read_only=True)
    answers = AnswerReviewSerializer(many=True, read_only=True)
    certificate_code = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentAttempt
        fields = [
            'id', 'assessment_title', 'course_title', 'course_slug', 'score',
            'total_points', 'percentage', 'passing_score', 'passed',
            'time_spent_seconds', 'started_at', 'submitted_at', 'certificate_code', 'answers'
        ]

    def get_certificate_code(self, obj):
        if obj.passed:
            cert = obj.user.certificates.filter(course=obj.assessment.course).first()
            return cert.certificate_code if cert else None
        return None

# Admin Serializers
class AdminOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = '__all__'

class AdminQuestionSerializer(serializers.ModelSerializer):
    options = AdminOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class AdminAssessmentSerializer(serializers.ModelSerializer):
    questions = AdminQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = '__all__'
