# serializers.py
from rest_framework import serializers
from .models import Notification, User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()
    display_name = serializers.CharField(max_length=100, read_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at', 'days_since_joined', 'display_name']
        read_only_fields = ['user_id', 'created_at', 'days_since_joined', 'display_name']
    
    def get_days_since_joined(self, obj):
        from django.utils.timezone import now
        return (now().date() - obj.created_at.date()).days
    
    def get_display_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_phone_number(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with country code (e.g., +1).")
        return value
    
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at', 'password']
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)
    content = serializers.CharField(
        max_length=200,
        required=True,
        allow_blank=False
    )
    is_recent = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'content', 'sent_at', 'is_recent']
        read_only_fields = ['message_id', 'sent_at', 'is_recent']
    
    def get_is_recent(self, obj):
        from django.utils.timezone import now
        from datetime import timedelta
        return (now() - obj.sent_at) < timedelta(hours=5)
        
    
    def validate_message_type(self, value):
        allowed_types = ['text', 'image', 'file', 'system']
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        if value not in allowed_types:
            raise serializers.ValidationError(f"Message type must be one of: {', '.join(allowed_types)}")
        return value

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'content', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'participant_count','created_at']
        read_only_fields = ['conversation_id', 'created_at', 'participant_count']
    
    def get_participant_count(self, obj):
        return obj.participants.count()


class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Conversation must have at least 2 participants.")
        
        # Check if all participant IDs exist
        existing_users = User.objects.filter(user_id__in=value)
        if len(existing_users) != len(value):
            raise serializers.ValidationError("One or more participant IDs are invalid.")
        
        return value

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participant_ids)
        return conversation
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_id', 'message', 'message_content', 'is_read', 'created_at']
        read_only_fields = ['notification_id', 'message_id', 'created_at']

    def validate_message(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Notification message cannot be empty.")
        