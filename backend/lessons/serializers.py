from rest_framework import serializers
from .models import Lesson, Vocabulary, Exercise


class VocabularySerializer(serializers.ModelSerializer):
    """Serializer for Vocabulary model."""
    
    class Meta:
        model = Vocabulary
        fields = [
            'id', 'word', 'translation', 'pronunciation',
            'example_sentence_de', 'example_sentence_en',
            'audio_url', 'image'
        ]


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for Exercise model."""
    
    class Meta:
        model = Exercise
        fields = [
            'id', 'exercise_type', 'question', 'correct_answer',
            'options', 'explanation', 'order'
        ]
        read_only_fields = ['correct_answer']  # Hide answer initially


class ExerciseSubmissionSerializer(serializers.Serializer):
    """Serializer for exercise answer submission."""
    
    exercise_id = serializers.IntegerField()
    user_answer = serializers.CharField()


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for Lesson model."""
    
    vocabulary = VocabularySerializer(many=True, read_only=True)
    exercises = ExerciseSerializer(many=True, read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    course_level = serializers.CharField(source='module.course.level', read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'lesson_type', 'content', 'order',
            'estimated_minutes', 'module_title', 'course_level',
            'vocabulary', 'exercises', 'created_at'
        ]


class LessonListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for lesson listings."""
    
    module_title = serializers.CharField(source='module.title', read_only=True)
    course_level = serializers.CharField(source='module.course.level', read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'lesson_type', 'estimated_minutes',
            'module_title', 'course_level', 'order'
        ]
