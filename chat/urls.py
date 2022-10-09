from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    # ex: /chat/
    path("", views.IndexView.as_view(), name="index"),
    path("conversations/", views.ConversationsView.as_view(), name="conversations"),
    path(
        "conversations/<int:pk>/",
        views.ConversationView.as_view(),
        name="conversation",
    ),
    path(
        "conversations/<int:pk>/send_message/",
        views.send_message,
        name="send_message",
    ),
]
