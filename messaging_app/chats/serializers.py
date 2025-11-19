# serializers.py
from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()
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


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(
        max_length=200,
        required=True,
        allow_blank=False
    )
    message_type = serializers.CharField(max_length=20, default='text')
    is_recent = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'message_type', 'sent_at', 'is_recent']
        read_only_fields = ['message_id', 'sent_at', 'is_recent']
    
    def get_is_recent(self, obj):
        from django.utils.timezone import now
        from datetime import timedelta
        return (now() - obj.sent_at) < timedelta(minutes=5)
    
    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
    
    def validate_message_type(self, value):
        allowed_types = ['text', 'image', 'file', 'system']
        if value not in allowed_types:
            raise serializers.ValidationError(f"Message type must be one of: {', '.join(allowed_types)}")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    conversation_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'participant_count', 'conversation_name', 'created_at']
        read_only_fields = ['conversation_id', 'created_at', 'participant_count']
    
    def get_participant_count(self, obj):
        return obj.participants.count()


class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    conversation_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids', 'conversation_name', 'created_at']
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