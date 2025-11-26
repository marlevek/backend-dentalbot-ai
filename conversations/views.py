from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Client
from .models import Conversation


@login_required
def conversations_list(request):
    client = Client.objects.get(user=request.user)
    conv = Conversation.objects.filter(client=client).order_by("-timestamp")

    return render(request, "conversations/list.html", {"conversations": conv})
