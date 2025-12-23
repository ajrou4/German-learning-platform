from django.db import models
from courses.models import Module


class Lesson(models.Model):
    """Lesson model for learning content."""
    
    LESSON_TYPE_CHOICES = [
        ('VOCABULARY', 'Vocabulary'),
        ('GRAMMAR', 'Grammar'),
        ('EXERCISE', 'Exercise'),
        ('READING', 'Reading'),
        ('LISTENING', 'Listening'),
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES)
    content = models.TextField()
    order = models.IntegerField(default=0)
    estimated_minutes = models.IntegerField(default=15)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lessons'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.course.level} - {self.title}"


class Vocabulary(models.Model):
    """Vocabulary words for lessons."""
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='vocabulary')
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=100, blank=True)
    example_sentence_de = models.TextField()
    example_sentence_en = models.TextField()
    audio_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='vocabulary/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vocabulary'
        verbose_name_plural = 'Vocabulary'
    
    def __str__(self):
        return f"{self.word} - {self.translation}"


class Exercise(models.Model):
    """Exercise questions for lessons."""
    
    EXERCISE_TYPE_CHOICES = [
        ('MULTIPLE_CHOICE', 'Multiple Choice'),
        ('FILL_BLANK', 'Fill in the Blank'),
        ('TRANSLATION', 'Translation'),
        ('MATCHING', 'Matching'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPE_CHOICES)
    question = models.TextField()
    correct_answer = models.TextField()
    options = models.JSONField(null=True, blank=True)  # For multiple choice
    explanation = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'exercises'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.lesson.title} - Exercise {self.order}"
