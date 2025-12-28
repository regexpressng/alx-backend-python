from rest_framework import viewsets, permissions
from rest_framework import permissions
from .permissions import IsParticipant
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ConversationFilter
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConversationFilter

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConversationCreateSerializer
        return ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        return Message.objects.filter(
            conversation__conversation_id=conversation_id,
            conversation__participants=self.request.user
        )

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user, conversation_id=self.kwargs.get('conversation_id'))
