from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.URLField(blank=True, null=True, max_length=500)
    headline = models.CharField(max_length=150, blank=True, null=True, default='Software Learner')
    bio = models.TextField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.get_full_name() or self.username})"

    @property
    def is_techspire_admin(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff
