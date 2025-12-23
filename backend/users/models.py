from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model for German Learning Platform."""
    
    LANGUAGE_LEVEL_CHOICES = [
        ('A1', 'Beginner A1'),
        ('A2', 'Elementary A2'),
        ('B1', 'Intermediate B1'),
        ('B2', 'Upper Intermediate B2'),
        ('C1', 'Advanced C1'),
        ('C2', 'Proficient C2'),
    ]
    
    NATIVE_LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('AR', 'Arabic'),
        ('ES', 'Spanish'),
        ('FR', 'French'),
        ('IT', 'Italian'),
        ('PT', 'Portuguese'),
        ('RU', 'Russian'),
        ('TR', 'Turkish'),
        ('ZH', 'Chinese'),
    ]
    
    email = models.EmailField(unique=True)
    language_level = models.CharField(
        max_length=2,
        choices=LANGUAGE_LEVEL_CHOICES,
        default='A1'
    )
    native_language = models.CharField(
        max_length=2,
        choices=NATIVE_LANGUAGE_CHOICES,
        default='EN'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Learning preferences
    daily_goal_minutes = models.IntegerField(default=30)
    notification_enabled = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
