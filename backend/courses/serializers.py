from rest_framework import serializers
from .models import Course, Module


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for Module model."""
    
    lesson_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'lesson_count']
    
    def get_lesson_count(self, obj):
        return obj.lessons.count()


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    
    modules = ModuleSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'level', 'thumbnail',
            'order', 'is_published', 'modules', 'total_lessons',
            'created_at', 'updated_at'
        ]
    
    def get_total_lessons(self, obj):
        from lessons.models import Lesson
        return Lesson.objects.filter(module__course=obj).count()


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for course listings."""
    
    total_lessons = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'level', 'thumbnail', 'total_lessons']
    
    def get_total_lessons(self, obj):
        from lessons.models import Lesson
        return Lesson.objects.filter(module__course=obj).count()
