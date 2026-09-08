import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techspire_core.settings')
django.setup()

from courses.models import Course

PRICE_MAP = {
    'python': {'title': 'Python Programming Mastery', 'price': 149900, 'original': 199900},
    'c-prog': {'title': 'C Systems Programming', 'price': 119900, 'original': 159900},
    'cpp': {'title': 'Modern C++ Architecture', 'price': 149900, 'original': 199900},
    'sql': {'title': 'SQL & Database Systems', 'price': 109900, 'original': 149900},
    'dsa': {'title': 'Data Structures & Algorithms', 'price': 149900, 'original': 199900},
    'oop': {'title': 'OOP & Design Patterns', 'price': 119900, 'original': 159900},
    'ai': {'title': 'Artificial Intelligence Fundamentals', 'price': 149900, 'original': 199900},
    'ml': {'title': 'Machine Learning Modeling', 'price': 199900, 'original': 249900},
    'os': {'title': 'Operating Systems Internals', 'price': 149900, 'original': 199900},
}

for course in Course.objects.all():
    matched = False
    for key, data in PRICE_MAP.items():
        if key in course.slug or data['title'].lower() in course.title.lower():
            course.price_in_paise = data['price']
            course.original_price_in_paise = data['original']
            course.discount_price_in_paise = data['price']
            course.is_free = False
            course.currency = 'INR'
            course.save(update_fields=['price_in_paise', 'original_price_in_paise', 'discount_price_in_paise', 'is_free', 'currency'])
            print(f"Updated {course.title} -> INR {course.price_in_rupees} (Original INR {course.original_price_in_rupees}, Save INR {course.discount_amount_in_rupees})")
            matched = True
            break
    if not matched:
        course.price_in_paise = 149900
        course.original_price_in_paise = 199900
        course.discount_price_in_paise = 149900
        course.is_free = False
        course.currency = 'INR'
        course.save()
        print(f"Default updated {course.title} -> INR {course.price_in_rupees}")

print("\nAll courses updated with production database pricing!")
