from django.db import models
from django.conf import settings


class ChatSession(models.Model):
    """Chat session with AI tutor."""
    
    MODE_CHOICES = [
        ('BEGINNER', 'Beginner Mode'),
        ('GRAMMAR', 'Grammar Explanation'),
        ('CONVERSATION', 'Conversation Practice'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='BEGINNER')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.mode} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        # Auto-generate title if not provided
        if not self.title:
            from django.utils import timezone
            now = self.created_at if self.created_at else timezone.now()
            self.title = f"{self.get_mode_display()} - {now.strftime('%b %d, %Y')}"
        super().save(*args, **kwargs)


class ChatMessage(models.Model):
    """Individual chat message."""
    
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ASSISTANT', 'AI Assistant'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    corrections = models.JSONField(null=True, blank=True)  # Store grammar corrections
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role} - {self.content[:50]}"
