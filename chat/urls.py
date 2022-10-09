from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    # ex: /chat/
    path("", views.IndexView.as_view(), name="index"),
    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name="logout"),
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
