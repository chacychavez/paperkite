from django.urls import path

from . import views

urlpatterns = [
    # ex: /chat/
    path("", views.index, name="index"),
    # ex: chat/conversations/
    path("conversations/", views.conversations, name="conversations"),
    # ex: /chat/conversations/5/
    path(
        "conversations/<int:conversation_id>/", views.conversation, name="conversation"
    ),
    # ex: /chat/conversations/5/messages/
    path(
        "conversations/<int:conversation_id>/messages/",
        views.messages,
        name="messages",
    ),
    # ex: /chat/conversations/5/messages/5/
    path(
        "conversations/<int:conversation_id>/messages/<int:message_id>/",
        views.message,
        name="message",
    ),
    # ex: /chat/conversations/5/send_message/
    path(
        "conversations/<int:conversation_id>/send_message/",
        views.send_message,
        name="send_message",
    ),
]
