from django.db import models
from django.conf import settings
from lessons.models import Lesson


class UserProgress(models.Model):
    """Track user progress through lessons."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress')
    completion_percentage = models.IntegerField(default=0)
    score = models.IntegerField(null=True, blank=True)
    time_spent_minutes = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_progress'
        unique_together = ['user', 'lesson']
        ordering = ['-last_accessed']
    
    def __str__(self):
        return f"{self.user.email} - {self.lesson.title} ({self.completion_percentage}%)"


class UserStreak(models.Model):
    """Track user learning streaks."""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='streak')
    streak_days = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_streaks'
    
    def __str__(self):
        return f"{self.user.email} - {self.streak_days} days"


class Achievement(models.Model):
    """Gamification achievements."""
    
    ACHIEVEMENT_TYPE_CHOICES = [
        ('LESSONS', 'Lessons Completed'),
        ('STREAK', 'Learning Streak'),
        ('VOCABULARY', 'Vocabulary Mastered'),
        ('LEVEL', 'Level Completed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'achievements'
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
