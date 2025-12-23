from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserProfileUpdateSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint."""
    
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserProfileUpdateSerializer
        return UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """Get user learning statistics."""
    user = request.user
    
    # Import here to avoid circular imports
    from progress.models import UserProgress, UserStreak
    
    total_lessons = UserProgress.objects.filter(user=user).count()
    completed_lessons = UserProgress.objects.filter(
        user=user,
        completion_percentage=100
    ).count()
    
    current_streak = UserStreak.objects.filter(user=user).first()
    
    return Response({
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'current_streak': current_streak.streak_days if current_streak else 0,
        'language_level': user.language_level,
    })
