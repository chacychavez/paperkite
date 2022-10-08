from django.contrib import admin

from .models import Conversation, ConversationUser, Message, User

admin.site.register([User, Conversation, ConversationUser, Message])
