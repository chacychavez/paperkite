from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View, generic

from .forms import CustomLoginForm, NewUserForm
from .models import ChatUser, Conversation, ConversationChatUser, Message


class IndexView(generic.TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("chat:conversations")
        else:
            return redirect("chat:login")


def login_request(request):
    if request.method == "POST":
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("chat:conversations")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(
        request=request, template_name="chat/login.html", context={"form": form}
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("chat:index")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("chat:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(
        request=request,
        template_name="chat/register.html",
        context={"form": form},
    )


@method_decorator(login_required, name="dispatch")
class ConversationsView(View):
    template_name = "chat/conversations.html"

    def get(self, request):
        user_id = request.user.id
        user_conversations = ConversationChatUser.objects.filter(
            chat_user_id=user_id
        ).values("conversation_id")
        conversations = []
        for user_converstation in user_conversations:
            conversation = Conversation.objects.get(
                pk=user_converstation.conversation_id
            )
            conversations.append(conversation)
        return render(request, self.template_name, {"converstations": conversations})

    def post(self, request):
        return redirect("chat:new_conversation")


@method_decorator(login_required, name="dispatch")
class ConversationView(View):
    template_name = "chat/conversation.html"

    def get(self, request, conversation_id):
        user_id = request.user.id
        user_conversations = ConversationChatUser.objects.filter(
            chat_user_id=user_id
        ).values("conversation_id")
        conversations = []
        for user_converstation in user_conversations:
            conversation = Conversation.objects.get(
                pk=user_converstation.conversation_id
            )
            conversations.append(conversation)
        messages = Message.objects.filter(conversation_id=conversation_id).order_by(
            "-sent_at"
        )
        return render(
            request,
            self.template_name,
            {
                "converstations": conversations,
                "conversation_id": conversation_id,
                "messages": messages,
            },
        )

    def post(self, request, conversation_id):
        # TODO: Send message
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        return render(
            request,
            "chat/conversation.html",
            {
                "conversation": conversation,
                "error_message": "You didn't type any message.",
            },
        )
        # try:
        #     selected_choice = conversation.choice_set.get(pk=request.POST["choice"])
        # except (KeyError, Choice.DoesNotExist):
        #     # Redisplay the question voting form.
        #     return render(
        #         request,
        #         "polls/detail.html",
        #         {
        #             "question": conversation,
        #             "error_message": "You didn't type any message.",
        #         },
        #     )
        # else:
        #     selected_choice.votes += 1
        #     selected_choice.save()
        #     # Always return an HttpResponseRedirect after successfully dealing
        #     # with POST data. This prevents data from being posted twice if a
        #     # user hits the Back button.
        #     return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        # response = f"You are sending a message to conversation {conversation_id}."
        # return HttpResponse(response)


class NewConversationView(View):
    template_name = "chat/conversations.html"

    def get(self, request):
        user_id = request.user.id
        user_conversations = ConversationChatUser.objects.filter(
            chat_user_id=user_id
        ).values("conversation_id")
        conversations = []
        for user_converstation in user_conversations:
            conversation = Conversation.objects.get(
                pk=user_converstation.conversation_id
            )
            conversations.append(conversation)
        users = ChatUser.objects.all()
        return render(
            request,
            self.template_name,
            {"converstations": conversations, "new": True, "users": users},
        )

    def post(self, request):
        pass
