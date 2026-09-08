from rest_framework import serializers
from .models import Category, Course, Module, Chapter

class CategorySerializer(serializers.ModelSerializer):
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'description', 'courses_count']

    def get_courses_count(self, obj):
        return obj.courses.filter(is_published=True).count()

class ChapterListSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'slug', 'order', 'duration_minutes', 'is_free_preview', 'is_completed']

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_progress.filter(user=request.user, is_completed=True).exists()
        return False

class ChapterDetailSerializer(serializers.ModelSerializer):
    module_id = serializers.IntegerField(source='module.id', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    course_slug = serializers.CharField(source='module.course.slug', read_only=True)
    course_title = serializers.CharField(source='module.course.title', read_only=True)
    is_completed = serializers.SerializerMethodField()
    next_chapter = serializers.SerializerMethodField()
    prev_chapter = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = [
            'id', 'title', 'slug', 'order', 'duration_minutes', 'is_free_preview',
            'content_markdown', 'code_snippet', 'code_language', 'key_takeaways',
            'practice_questions', 'module_id', 'module_title', 'course_slug', 'course_title',
            'is_completed', 'next_chapter', 'prev_chapter', 'created_at', 'updated_at'
        ]

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_progress.filter(user=request.user, is_completed=True).exists()
        return False

    def get_next_chapter(self, obj):
        # Same module next chapter
        next_ch = Chapter.objects.filter(module=obj.module, order__gt=obj.order).order_by('order').first()
        if not next_ch:
            # Next module first chapter
            next_mod = Module.objects.filter(course=obj.module.course, order__gt=obj.module.order).order_by('order').first()
            if next_mod:
                next_ch = next_mod.chapters.order_by('order').first()
        if next_ch:
            return {'id': next_ch.id, 'title': next_ch.title, 'slug': next_ch.slug}
        return None

    def get_prev_chapter(self, obj):
        # Same module prev chapter
        prev_ch = Chapter.objects.filter(module=obj.module, order__lt=obj.order).order_by('-order').first()
        if not prev_ch:
            # Prev module last chapter
            prev_mod = Module.objects.filter(course=obj.module.course, order__lt=obj.module.order).order_by('-order').first()
            if prev_mod:
                prev_ch = prev_mod.chapters.order_by('-order').first()
        if prev_ch:
            return {'id': prev_ch.id, 'title': prev_ch.title, 'slug': prev_ch.slug}
        return None

class ModuleSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'chapters']

    def get_chapters(self, obj):
        chapters = obj.chapters.all().order_by('order')
        return ChapterListSerializer(chapters, many=True, context=self.context).data

class CourseListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_modules = serializers.IntegerField(read_only=True)
    total_chapters = serializers.IntegerField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    price_in_rupees = serializers.IntegerField(read_only=True)
    original_price_in_rupees = serializers.IntegerField(read_only=True)
    discount_amount_in_rupees = serializers.IntegerField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'tagline', 'description', 'category', 'category_name',
            'difficulty', 'estimated_hours', 'cover_image', 'badge_icon', 'color_accent',
            'price_in_paise', 'original_price_in_paise', 'discount_price_in_paise', 'currency', 'is_free',
            'price_in_rupees', 'original_price_in_rupees', 'discount_amount_in_rupees', 'discount_percentage',
            'total_modules', 'total_chapters', 'is_enrolled', 'progress_percentage', 'created_at'
        ]

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(user=request.user).exists()
        return False

    def get_progress_percentage(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            enrollment = obj.enrollments.filter(user=request.user).first()
            if enrollment:
                return enrollment.calculate_progress()
        return 0

class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    modules = serializers.SerializerMethodField()
    total_modules = serializers.IntegerField(read_only=True)
    total_chapters = serializers.IntegerField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    has_assessment = serializers.SerializerMethodField()
    price_in_rupees = serializers.IntegerField(read_only=True)
    original_price_in_rupees = serializers.IntegerField(read_only=True)
    discount_amount_in_rupees = serializers.IntegerField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'tagline', 'description', 'category',
            'difficulty', 'estimated_hours', 'cover_image', 'badge_icon',
            'color_accent', 'is_published', 'prerequisites', 'learning_outcomes',
            'price_in_paise', 'original_price_in_paise', 'discount_price_in_paise', 'currency', 'is_free',
            'price_in_rupees', 'original_price_in_rupees', 'discount_amount_in_rupees', 'discount_percentage',
            'total_modules', 'total_chapters', 'is_enrolled', 'progress_percentage',
            'has_assessment', 'modules', 'created_at', 'updated_at'
        ]

    def get_modules(self, obj):
        modules = obj.modules.all().order_by('order')
        return ModuleSerializer(modules, many=True, context=self.context).data

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(user=request.user).exists()
        return False

    def get_progress_percentage(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            enrollment = obj.enrollments.filter(user=request.user).first()
            if enrollment:
                return enrollment.calculate_progress()
        return 0

    def get_has_assessment(self, obj):
        return hasattr(obj, 'assessment') and obj.assessment.is_published

# Admin CRUD serializers
class AdminCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, attrs):
        price = attrs.get('price_in_paise', getattr(self.instance, 'price_in_paise', 0))
        orig_price = attrs.get('original_price_in_paise', getattr(self.instance, 'original_price_in_paise', None))
        is_free = attrs.get('is_free', getattr(self.instance, 'is_free', False))

        if not is_free and price < 0:
            raise serializers.ValidationError({"price_in_paise": "Course price cannot be negative."})

        if orig_price is not None and orig_price < price and not is_free:
            raise serializers.ValidationError({"original_price_in_paise": "Original price cannot be less than selling price."})

        return attrs

class AdminModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class AdminChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
