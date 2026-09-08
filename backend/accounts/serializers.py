from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'avatar', 'headline', 'bio', 'github', 'linkedin',
            'created_at', 'updated_at', 'is_staff', 'is_superuser'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_staff', 'is_superuser']

import re

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_blank=True, default='')
    first_name = serializers.CharField(required=False, allow_blank=True, default='')
    last_name = serializers.CharField(required=False, allow_blank=True, default='')
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate_email(self, value):
        normalized_email = value.lower().strip()
        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError("An account with this email address already exists. Please sign in instead.")
        return normalized_email

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        email = validated_data['email'].lower().strip()
        raw_username = validated_data.get('username', '').strip() or email.split('@')[0]
        
        # Sanitize username into valid chars
        base_username = re.sub(r'[^a-zA-Z0-9_]', '_', raw_username).strip('_') or 'student'
        username = base_username
        counter = 1
        while User.objects.filter(username__iexact=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        user = User.objects.create_user(
            email=email,
            username=username,
            first_name=validated_data.get('first_name', '').strip(),
            last_name=validated_data.get('last_name', '').strip(),
            password=validated_data['password'],
            role='student'
        )
        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'headline', 'bio', 'github', 'linkedin']

class AdminUserManageSerializer(serializers.ModelSerializer):
    total_enrollments = serializers.SerializerMethodField()
    total_certificates = serializers.SerializerMethodField()
    total_attempts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'avatar', 'headline', 'bio', 'is_active',
            'created_at', 'last_login', 'total_enrollments',
            'total_certificates', 'total_attempts'
        ]

    def get_total_enrollments(self, obj):
        return obj.enrollments.count()

    def get_total_certificates(self, obj):
        return obj.certificates.count()

    def get_total_attempts(self, obj):
        return obj.assessment_attempts.count()
