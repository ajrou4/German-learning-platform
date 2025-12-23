from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    
    list_display = ['email', 'username', 'language_level', 'native_language', 'created_at']
    list_filter = ['language_level', 'native_language', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Learning Profile', {
            'fields': ('language_level', 'native_language', 'profile_picture', 'bio')
        }),
        ('Preferences', {
            'fields': ('daily_goal_minutes', 'notification_enabled')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Learning Profile', {
            'fields': ('language_level', 'native_language')
        }),
    )
