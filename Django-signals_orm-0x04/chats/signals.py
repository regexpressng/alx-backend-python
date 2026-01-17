from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, User, Conversation
import logging

logger = logging.getLogger(__name__)

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

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                logger.info(f"Message {instance.pk} content changed from '{old_instance.content}' to '{instance.content}'") 
                from .models import MessageHistory
                MessageHistory.objects.create(
                    message=old_instance,
                    edited_content=old_instance.content
                )
            else:
                logger.info(f"Message {instance.content} content unchanged.") 
        except Message.DoesNotExist:
            logger.info(f"Message {instance.pk} does not exist in the database.")

@receiver(post_delete, sender=User)
def cleanup_conversations(sender, instance, **kwargs):
    conversations = Conversation.objects.filter(participants=instance)
    for convo in conversations:
        if convo.participants.count() <= 1:
            convo.delete()
