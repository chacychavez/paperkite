from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


@receiver(post_save, sender=User)
def create_chat_user(sender, instance, created, **kwargs):
    if created:
        ChatUser.objects.create(user=instance)


class ChatUser(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "PUB", _("Public")
        PRIVATE = "PVT", _("Private")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visibility = models.CharField(
        max_length=3,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
    )
    updated_at = models.DateTimeField(auto_now=True)


class Conversation(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConversationChatUser(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    chat_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(default=None)


class Message(models.Model):
    class Status(models.TextChoices):
        SENT = "SENT", _("Sent")
        SEEN = "SEEN", _("Seen")

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    chat_user = models.ForeignKey(ChatUser, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=512)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.SENT,
    )
