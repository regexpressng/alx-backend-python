# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Allows access only to users who are participants of a conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be a Conversation or a Message
        if hasattr(obj, 'participants'):
            # Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # Message
            return request.user in obj.conversation.participants.all()
        return False