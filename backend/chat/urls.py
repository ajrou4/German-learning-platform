from django.urls import path
from .views import (
    ChatSessionListView,
    ChatSessionDetailView,
    send_message,
    clear_session
)

urlpatterns = [
    path('sessions/', ChatSessionListView.as_view(), name='chat_sessions'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='chat_session_detail'),
    path('send/', send_message, name='send_message'),
    path('sessions/<int:pk>/clear/', clear_session, name='clear_session'),
]
