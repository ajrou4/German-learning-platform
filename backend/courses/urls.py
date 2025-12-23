from django.urls import path
from .views import CourseListView, CourseDetailView, ModuleDetailView

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),
]
