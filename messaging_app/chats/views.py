# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    queryset = Conversation.objects.prefetch_related('participants', 'messages__sender').all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        # Use a different serializer for creation
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        # Automatically include the current user in the conversation
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()

    @action(detail=True, methods=['get'], url_path='messages')
    def list_messages(self, request, pk=None):
        """List all messages in a given conversation."""
        conversation = self.get_object()
        messages = conversation.messages.select_related('sender').all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for sending and listing messages.
    """
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically set the sender to the current user."""
        serializer.save(sender=self.request.user)
