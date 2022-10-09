from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Conversation


class IndexView(generic.TemplateView):
    template_name = "chat/index.html"


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
