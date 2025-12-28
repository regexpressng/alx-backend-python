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
    conversation_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True,db_index=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.CharField(max_length=200, null=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender}"
