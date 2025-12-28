from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    of a conversation or messages belonging to a conversation they are in.
    Only participants can update or delete (PUT, PATCH, DELETE).
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Everyone can GET (read) if they're a participant
        if hasattr(obj, 'participants'):
            # obj is a Conversation
            is_participant = request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # obj is a Message
            is_participant = request.user in obj.conversation.participants.all()
        else:
            return False

        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return is_participant
        else:  # PUT, PATCH, DELETE
            return is_participant  # Only participants can modify/delete
