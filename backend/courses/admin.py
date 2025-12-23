from django.contrib import admin
from .models import Course, Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'order', 'is_published', 'created_at']
    list_filter = ['level', 'is_published']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_published']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course']
    search_fields = ['title', 'description']
    list_editable = ['order']
