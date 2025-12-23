from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Course, Module
from .serializers import CourseSerializer, CourseListSerializer, ModuleSerializer


class CourseListView(generics.ListAPIView):
    """List all published courses."""
    
    permission_classes = [AllowAny]
    serializer_class = CourseListSerializer
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True)
        level = self.request.query_params.get('level', None)
        if level:
            queryset = queryset.filter(level=level)
        return queryset


class CourseDetailView(generics.RetrieveAPIView):
    """Get course details with modules and lessons."""
    
    permission_classes = [AllowAny]
    serializer_class = CourseSerializer
    queryset = Course.objects.filter(is_published=True)


class ModuleDetailView(generics.RetrieveAPIView):
    """Get module details."""
    
    permission_classes = [AllowAny]
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
