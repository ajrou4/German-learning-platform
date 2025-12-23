from rest_framework import serializers
from .models import UserProgress, UserStreak, Achievement


class UserProgressSerializer(serializers.ModelSerializer):
    """Serializer for UserProgress model."""
    
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    lesson_type = serializers.CharField(source='lesson.lesson_type', read_only=True)
    
    class Meta:
        model = UserProgress
        fields = [
            'id', 'lesson', 'lesson_title', 'lesson_type',
            'completion_percentage', 'score', 'time_spent_minutes',
            'started_at', 'completed_at', 'last_accessed'
        ]
        read_only_fields = ['started_at', 'last_accessed']


class UserStreakSerializer(serializers.ModelSerializer):
    """Serializer for UserStreak model."""
    
    class Meta:
        model = UserStreak
        fields = ['streak_days', 'longest_streak', 'last_activity_date']


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for Achievement model."""
    
    class Meta:
        model = Achievement
        fields = ['id', 'achievement_type', 'title', 'description', 'icon', 'earned_at']
