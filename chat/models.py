from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = "PUB", _("Public")
        PRIVATE = "PVT", _("Private")

    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    email_address = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(
        max_length=3,
        choices=Visibility.choices,
        default=Visibility.PUBLIC,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Conversation(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConversationUser(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(default=None)


class Message(models.Model):
    class Status(models.TextChoices):
        SENT = "SENT", _("Sent")
        SEEN = "SEEN", _("Seen")

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=512)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=4,
        choices=Status.choices,
        default=Status.SENT,
    )
