# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipant
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
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConversationCreateSerializer
        return ConversationSerializer
    

class MessageViewSet(viewsets.ModelViewSet):
    """
        Viewset to retrieve messages
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant]

    def get_queryset(self):
        # Get conversation_id from URL kwargs (nested router)
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation__conversation_id=conversation_id)

    def perform_create(self, serializer):
        # Automatically set the sender to the logged-in user
        serializer.save(sender=self.request.user)
