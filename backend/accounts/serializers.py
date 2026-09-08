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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username') or validated_data['email'].split('@')[0],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
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
