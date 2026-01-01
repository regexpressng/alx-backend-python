from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        participants = instance.conversation.participants.exclude(user_id=instance.sender.user_id)
        
        notifications = []
        for participant in participants:
            notifications.append(Notification(
                participant=participant,
                message=instance,
                message_content=f"New message from {instance.sender.email}: {instance.content}"
            ))
            Notification.objects.bulk_create(notifications)
