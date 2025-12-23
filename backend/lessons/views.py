from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Lesson, Exercise
from .serializers import (
    LessonSerializer,
    LessonListSerializer,
    ExerciseSubmissionSerializer
)


class LessonListView(generics.ListAPIView):
    """List all published lessons."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = LessonListSerializer
    
    def get_queryset(self):
        queryset = Lesson.objects.filter(is_published=True)
        
        # Filter by module
        module_id = self.request.query_params.get('module', None)
        if module_id:
            queryset = queryset.filter(module_id=module_id)
        
        # Filter by level
        level = self.request.query_params.get('level', None)
        if level:
            queryset = queryset.filter(module__course__level=level)
        
        return queryset


class LessonDetailView(generics.RetrieveAPIView):
    """Get lesson details with vocabulary and exercises."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.filter(is_published=True)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_exercise(request):
    """Submit exercise answer and get feedback."""
    
    serializer = ExerciseSubmissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    exercise_id = serializer.validated_data['exercise_id']
    user_answer = serializer.validated_data['user_answer']
    
    exercise = get_object_or_404(Exercise, id=exercise_id)
    
    is_correct = user_answer.strip().lower() == exercise.correct_answer.strip().lower()
    
    # Update user progress
    from progress.models import UserProgress
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=exercise.lesson
    )
    
    return Response({
        'is_correct': is_correct,
        'correct_answer': exercise.correct_answer if not is_correct else None,
        'explanation': exercise.explanation,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_lesson(request, pk):
    """Mark lesson as completed."""
    
    lesson = get_object_or_404(Lesson, pk=pk)
    
    from progress.models import UserProgress
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    progress.completion_percentage = 100
    progress.completed_at = models.DateTimeField(auto_now=True)
    progress.save()
    
    return Response({
        'message': 'Lesson completed successfully',
        'progress': progress.completion_percentage
    })
