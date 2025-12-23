from django.contrib import admin
from .models import UserProgress, UserStreak, Achievement


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completion_percentage', 'score', 'last_accessed']
    list_filter = ['completion_percentage', 'lesson__lesson_type']
    search_fields = ['user__email', 'lesson__title']


@admin.register(UserStreak)
class UserStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'streak_days', 'longest_streak', 'last_activity_date']
    search_fields = ['user__email']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'achievement_type', 'earned_at']
    list_filter = ['achievement_type', 'earned_at']
    search_fields = ['user__email', 'title']
