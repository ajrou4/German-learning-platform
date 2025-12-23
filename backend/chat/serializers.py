from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for ChatMessage model."""
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'role', 'content', 'corrections', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatSessionSerializer(serializers.ModelSerializer):
    """Serializer for ChatSession model."""
    
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = [
            'id', 'mode', 'title', 'is_active',
            'created_at', 'updated_at', 'messages', 'message_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()


class ChatSessionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for chat session listings."""
    
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = [
            'id', 'mode', 'title', 'is_active',
            'created_at', 'updated_at', 'message_count', 'last_message'
        ]
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'content': last_msg.content[:100],
                'role': last_msg.role,
                'created_at': last_msg.created_at
            }
        return None


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending a chat message."""
    
    session_id = serializers.IntegerField(required=False, allow_null=True)
    mode = serializers.ChoiceField(
        choices=['BEGINNER', 'GRAMMAR', 'CONVERSATION'],
        required=False,
        default='BEGINNER'
    )
    message = serializers.CharField()
