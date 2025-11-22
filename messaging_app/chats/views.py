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


class ConversationViewSet(viewsets.ViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    def list(self):
        queryset = Conversation.objects.all()
        serializer =  ConversationSerializer(queryset)
        return Response(serializer.data)
    

class MessageViewSet(viewsets.ViewSet):
    """
        Viewset to retrieve messages
    """
    def retrieve(self, request, conversation_id=None):
        queryset = Message.objects.filter( conversation__conversation_id=conversation_id)
        serializer = MessageSerializer(queryset)
        return Response(serializer)
