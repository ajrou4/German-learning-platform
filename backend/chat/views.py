from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer,
    ChatSessionListSerializer,
    ChatMessageSerializer,
    SendMessageSerializer
)
from ai_engine.services import GermanTutor


class ChatSessionListView(generics.ListCreateAPIView):
    """List all chat sessions or create a new one."""
    
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatSessionSerializer
        return ChatSessionListSerializer
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a chat session."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSessionSerializer
    
    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    Send a message to AI tutor.
    
    POST data:
        session_id: Optional, chat session ID
        mode: Optional, chat mode (BEGINNER, GRAMMAR, CONVERSATION)
        message: User's message
    """
    
    serializer = SendMessageSerializer(data=request.data)
    if not serializer.is_valid():
        print(f"Validation errors: {serializer.errors}")
        print(f"Request data: {request.data}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.is_valid(raise_exception=True)
    
    session_id = serializer.validated_data.get('session_id')
    mode = serializer.validated_data.get('mode', 'BEGINNER')
    user_message = serializer.validated_data['message']
    
    # Get or create session
    if session_id:
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    else:
        session = ChatSession.objects.create(
            user=request.user,
            mode=mode
        )
    
    # Save user message
    user_msg = ChatMessage.objects.create(
        session=session,
        role='USER',
        content=user_message
    )
    
    # Get conversation history
    history = []
    for msg in session.messages.all()[:20]:  # Last 20 messages
        history.append({
            'role': 'user' if msg.role == 'USER' else 'assistant',
            'content': msg.content
        })
    
    # Get AI response
    ai_response = GermanTutor.chat(
        message=user_message,
        conversation_history=history[:-1],  # Exclude the message we just added
        mode=session.mode.lower(),
        user_level=request.user.language_level
    )
    
    # Save AI response
    ai_msg = ChatMessage.objects.create(
        session=session,
        role='ASSISTANT',
        content=ai_response
    )
    
    return Response({
        'session_id': session.id,
        'user_message': ChatMessageSerializer(user_msg).data,
        'ai_response': ChatMessageSerializer(ai_msg).data,
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_session(request, pk):
    """Clear all messages in a chat session."""
    
    session = get_object_or_404(ChatSession, id=pk, user=request.user)
    session.messages.all().delete()
    
    return Response({
        'message': 'Chat session cleared successfully'
    })
