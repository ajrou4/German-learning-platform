from django.db import models


class Course(models.Model):
    """Course model for organizing lessons."""
    
    LEVEL_CHOICES = [
        ('A1', 'Beginner A1'),
        ('A2', 'Elementary A2'),
        ('B1', 'Intermediate B1'),
        ('B2', 'Upper Intermediate B2'),
        ('C1', 'Advanced C1'),
        ('C2', 'Proficient C2'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        ordering = ['level', 'order']
    
    def __str__(self):
        return f"{self.level} - {self.title}"


class Module(models.Model):
    """Module model for grouping lessons within a course."""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'modules'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
