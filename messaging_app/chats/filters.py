# chats/filters.py
import django_filters
from .models import Message, Conversation

class MessageFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    end_time = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ['start_time', 'end_time']

class ConversationFilter(django_filters.FilterSet):
    participant = django_filters.UUIDFilter(
        field_name="participants__user_id"
    )

    class Meta:
        model = Conversation
        fields = ['participant']
