# models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings


class UserRoles(models.TextChoices):
    GUEST = 'guest', 'Guest'
    HOST = 'host', 'Host'
    ADMIN = 'admin', 'Admin'
    MODERATOR = 'moderator','Moderator'
DEFAULT_ROLE = UserRoles.GUEST

class User(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False
    )
    phone_number = models.CharField(
        max_length=50, 
        unique=True, 
        null=False
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        db_index=True
    )

    password_hash = models.CharField(
        max_length=128,
        blank=False,
        null=False
    )

    role = models.CharField(
        max_length=10,
        choices=UserRoles.choices,
        default=DEFAULT_ROLE,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number', 'password_hash']


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True,db_index=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    content = models.CharField(max_length=200, null=False, default='')
    sent_at = models.DateTimeField(default=timezone.now)

    # New field for threaded replies
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    def __str__(self):
        return f"Message from {self.sender}"

    
class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications', null=True)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message_content = models.CharField(max_length=255, null=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
            ordering = ['-created_at']      
    def __str__(self):
        return f"Notification for {self.user.username}"

class MessageHistory(models.Model):
    history_id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    edited_content = models.CharField(max_length=200, null=False)
    edited_at = models.DateTimeField(default=timezone.now)

    class Meta:
            ordering = ['-edited_at']      
    def __str__(self):
        return f"History for Message {self.message.message_id}"
