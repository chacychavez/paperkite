from django.urls import path

from .views import (
    ConversationsView,
    ConversationView,
    IndexView,
    login_request,
    logout_request,
    register_request,
    send_message,
)

app_name = "chat"
urlpatterns = [
    # ex: /chat/
    path("", IndexView.as_view(), name="index"),
    path("login/", login_request, name="login"),
    path("register/", register_request, name="register"),
    path("logout/", logout_request, name="logout"),
    path("conversations/", ConversationsView.as_view(), name="conversations"),
    path(
        "conversations/<int:pk>/",
        ConversationView.as_view(),
        name="conversation",
    ),
    path(
        "conversations/<int:pk>/send_message/",
        send_message,
        name="send_message",
    ),
]
