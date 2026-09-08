from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=50, default='Code')
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Course(models.Model):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    tagline = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    estimated_hours = models.IntegerField(default=20)
    cover_image = models.URLField(blank=True, null=True, max_length=500)
    badge_icon = models.CharField(max_length=50, default='Terminal')
    color_accent = models.CharField(max_length=30, default='#06B6D4')
    
    # Pricing fields in paise (integer-safe currency storage, 1 INR = 100 paise)
    price_in_paise = models.IntegerField(default=149900, help_text="Selling price in paise (e.g. 149900 for ₹1,499)")
    original_price_in_paise = models.IntegerField(default=199900, blank=True, null=True, help_text="Original price in paise before discount (e.g. 199900 for ₹1,999)")
    discount_price_in_paise = models.IntegerField(default=149900, blank=True, null=True, help_text="Discounted selling price in paise")
    currency = models.CharField(max_length=10, default='INR')
    is_free = models.BooleanField(default=False)
    
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    prerequisites = models.JSONField(default=list, blank=True)
    learning_outcomes = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def price_in_rupees(self):
        return self.price_in_paise // 100 if self.price_in_paise else 0

    @property
    def original_price_in_rupees(self):
        return self.original_price_in_paise // 100 if self.original_price_in_paise else 0

    @property
    def discount_amount_in_rupees(self):
        if self.original_price_in_rupees > self.price_in_rupees:
            return self.original_price_in_rupees - self.price_in_rupees
        return 0

    @property
    def discount_percentage(self):
        if self.original_price_in_paise and self.original_price_in_paise > self.price_in_paise:
            return round(((self.original_price_in_paise - self.price_in_paise) / self.original_price_in_paise) * 100)
        return 0

    @property
    def total_modules(self):
        return self.modules.count()

    @property
    def total_chapters(self):
        return Chapter.objects.filter(module__course=self).count()

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.course.title} -> Module {self.order}: {self.title}"

class Chapter(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True)
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=15)
    is_free_preview = models.BooleanField(default=False)
    
    # Rich technical notes content
    content_markdown = models.TextField()
    code_snippet = models.TextField(blank=True, null=True)
    code_language = models.CharField(max_length=30, default='python')
    key_takeaways = models.JSONField(default=list, blank=True)
    practice_questions = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('module', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.module.course.title} -> {self.module.title} -> {self.title}"
