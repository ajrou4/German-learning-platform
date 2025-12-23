from django.urls import path
from .views import LessonListView, LessonDetailView, submit_exercise, complete_lesson

urlpatterns = [
    path('', LessonListView.as_view(), name='lesson_list'),
    path('<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('<int:pk>/complete/', complete_lesson, name='complete_lesson'),
    path('exercises/submit/', submit_exercise, name='submit_exercise'),
]
