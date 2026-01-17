from rest_framework import viewsets, permissions
from rest_framework import permissions
from .permissions import IsParticipant
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from .filters import ConversationFilter
from .models import Conversation, Message, Notification, User
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageCreateSerializer,
    MessageSerializer,
    NotificationSerializer,
    CreateUserSerializer, 
    UserSerializer,
    ThreadedMessageSerializer
)
from .pagination import MessagePagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

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
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_pk']
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user,
            parent_message__isnull=True  # only top-level messages
        ).select_related('sender').prefetch_related('replies__sender').order_by('-sent_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return ThreadedMessageSerializer

    def perform_create(self, serializer):
        conversation = get_object_or_404(
            Conversation,
            conversation_id=self.kwargs['conversation_pk']
        )
        serializer.save(conversation=conversation, sender=self.request.user)



class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.user_id
        return User.objects.filter(user_id=user_id).order_by('user_id')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer
    

    
