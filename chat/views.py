from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Conversation, Message


def index(request):
    return render(request, "chat/index.html")


def conversations(request):
    conversations = Conversation.objects.order_by("-updated_at")
    context = dict(conversations=conversations)
    return render(request, "chat/conversations.html", context)


def conversation(request, conversation_id):
    # try:
    #     conversation = Conversation.objects.get(pk=conversation_id)
    # except Conversation.DoesNotExist:
    #     raise Http404("Conversation does not exist")
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    return render(request, "chat/conversation.html", dict(conversation=conversation))


def messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)

    messages = Message.objects.filter(conversation_id=conversation.id).order_by(
        "-sent_at"
    )
    context = dict(messages=messages)
    return render(request, "chat/messages.html", context)


def message(request, conversation_id, message_id):
    get_object_or_404(Conversation, pk=conversation_id)
    message = get_object_or_404(Message, pk=message_id)
    return render(request, "chat/message.html", dict(message=message))


def send_message(request, conversation_id):
    response = f"You are sending a message to conversation {conversation_id}."
    return HttpResponse(response)
