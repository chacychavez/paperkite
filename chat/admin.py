from django.contrib import admin

from .models import ChatUser, Conversation, ConversationChatUser, Message

admin.site.register([ChatUser, Conversation, ConversationChatUser, Message])
