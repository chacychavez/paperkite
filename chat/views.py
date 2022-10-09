from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .forms import NewUserForm
from .models import Conversation


class IndexView(generic.TemplateView):
    template_name = "chat/index.html"


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("chat:index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="chat/login.html", context={"login_form": form}
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
    form = NewUserForm()
    return render(
        request=request,
        template_name="chat/register.html",
        context={"register_form": form},
    )


class ConversationsView(generic.ListView):
    template_name = "chat/conversations.html"
    context_object_name = "conversations"

    def get_queryset(self):
        """Return conversations odered by datetime."""
        return Conversation.objects.order_by("-updated_at")


class ConversationView(generic.DetailView):
    model = Conversation
    template_name = "chat/conversation.html"


def send_message(request, conversation_id):
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
