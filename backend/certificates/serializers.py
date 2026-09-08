from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='user.get_full_name', read_only=True)
    student_email = serializers.CharField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    course_badge = serializers.CharField(source='course.badge_icon', read_only=True)
    category_name = serializers.CharField(source='course.category.name', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'certificate_code', 'student_name', 'student_email',
            'course_title', 'course_slug', 'course_badge', 'category_name',
            'grade_percentage', 'issue_date', 'is_valid', 'verification_hash'
        ]

class PublicCertificateVerifySerializer(serializers.ModelSerializer):
    recipient_name = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    course_difficulty = serializers.CharField(source='course.difficulty', read_only=True)
    estimated_hours = serializers.IntegerField(source='course.estimated_hours', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'certificate_code', 'recipient_name', 'course_title',
            'course_slug', 'course_difficulty', 'estimated_hours',
            'grade_percentage', 'issue_date', 'is_valid', 'verification_hash'
        ]

    def get_recipient_name(self, obj):
        # Return full name or sanitized initial + last name for privacy
        name = obj.user.get_full_name()
        if name:
            return name
        return obj.user.username
