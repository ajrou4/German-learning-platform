from django.contrib import admin
from .models import Lesson, Vocabulary, Exercise


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'lesson_type', 'order', 'is_published']
    list_filter = ['lesson_type', 'is_published', 'module__course__level']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_published']


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ['word', 'translation', 'lesson']
    list_filter = ['lesson__module__course__level']
    search_fields = ['word', 'translation']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'exercise_type', 'order']
    list_filter = ['exercise_type', 'lesson__module__course__level']
    list_editable = ['order']
