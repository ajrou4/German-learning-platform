from django.urls import path
from .views import (
    UserProgressListView,
    UserProgressDetailView,
    user_streak,
    AchievementListView,
    dashboard_stats
)

urlpatterns = [
    path('', UserProgressListView.as_view(), name='progress_list'),
    path('<int:pk>/', UserProgressDetailView.as_view(), name='progress_detail'),
    path('streak/', user_streak, name='user_streak'),
    path('achievements/', AchievementListView.as_view(), name='achievements'),
    path('dashboard/', dashboard_stats, name='dashboard_stats'),
]
