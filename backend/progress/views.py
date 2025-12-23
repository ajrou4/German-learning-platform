from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from datetime import timedelta

from .models import UserProgress, UserStreak, Achievement
from .serializers import (
    UserProgressSerializer,
    UserStreakSerializer,
    AchievementSerializer
)


class UserProgressListView(generics.ListAPIView):
    """List user's progress for all lessons."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserProgressSerializer
    
    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)


class UserProgressDetailView(generics.RetrieveAPIView):
    """Get progress for a specific lesson."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserProgressSerializer
    
    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_streak(request):
    """Get user's learning streak."""
    
    streak, created = UserStreak.objects.get_or_create(user=request.user)
    
    # Update streak if user was active today
    today = timezone.now().date()
    if streak.last_activity_date < today:
        # Check if streak should continue
        yesterday = today - timedelta(days=1)
        if streak.last_activity_date == yesterday:
            streak.streak_days += 1
            if streak.streak_days > streak.longest_streak:
                streak.longest_streak = streak.streak_days
        else:
            # Streak broken
            streak.streak_days = 1
        
        streak.last_activity_date = today
        streak.save()
    
    serializer = UserStreakSerializer(streak)
    return Response(serializer.data)


class AchievementListView(generics.ListAPIView):
    """List user's achievements."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = AchievementSerializer
    
    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get comprehensive dashboard statistics."""
    
    user = request.user
    
    # Progress stats
    total_progress = UserProgress.objects.filter(user=user).count()
    completed = UserProgress.objects.filter(user=user, completion_percentage=100).count()
    in_progress = UserProgress.objects.filter(
        user=user,
        completion_percentage__gt=0,
        completion_percentage__lt=100
    ).count()
    
    # Streak
    streak, _ = UserStreak.objects.get_or_create(user=user)
    
    # Recent achievements
    recent_achievements = Achievement.objects.filter(user=user)[:5]
    
    # Time spent this week
    week_ago = timezone.now() - timedelta(days=7)
    time_this_week = UserProgress.objects.filter(
        user=user,
        last_accessed__gte=week_ago
    ).aggregate(total=models.Sum('time_spent_minutes'))['total'] or 0
    
    return Response({
        'total_lessons_started': total_progress,
        'lessons_completed': completed,
        'lessons_in_progress': in_progress,
        'current_streak': streak.streak_days,
        'longest_streak': streak.longest_streak,
        'time_this_week_minutes': time_this_week,
        'recent_achievements': AchievementSerializer(recent_achievements, many=True).data,
        'language_level': user.language_level,
    })
