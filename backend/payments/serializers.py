from rest_framework import serializers
from .models import PaymentOrder, Payment
from courses.models import Course

class PaymentOrderResponseSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    amount_in_rupees = serializers.IntegerField(read_only=True)

    class Meta:
        model = PaymentOrder
        fields = [
            'id', 'razorpay_order_id', 'amount', 'amount_in_rupees',
            'currency', 'status', 'course_title', 'course_slug', 'created_at'
        ]

class PaymentHistorySerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_slug = serializers.CharField(source='course.slug', read_only=True)
    course_cover = serializers.CharField(source='course.cover_image', read_only=True)
    course_difficulty = serializers.CharField(source='course.difficulty', read_only=True)
    order_id = serializers.CharField(source='payment_order.razorpay_order_id', read_only=True)
    amount_in_rupees = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'razorpay_payment_id', 'order_id', 'course_title', 'course_slug',
            'course_cover', 'course_difficulty', 'amount', 'amount_in_rupees',
            'currency', 'status', 'method', 'captured_at', 'created_at'
        ]

class AdminPaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    student_email = serializers.CharField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    order_id = serializers.CharField(source='payment_order.razorpay_order_id', read_only=True)
    amount_in_rupees = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'razorpay_payment_id', 'order_id', 'student_name', 'student_email',
            'course_title', 'amount', 'amount_in_rupees', 'currency', 'status',
            'method', 'captured_at', 'created_at'
        ]

    def get_student_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
