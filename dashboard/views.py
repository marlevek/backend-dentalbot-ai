from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Client
from conversations.models import Conversation


@login_required
def dashboard_home(request):
    client = Client.objects.get(user=request.user)

    total_conversations = Conversation.objects.filter(client=client).count()
    last_messages = Conversation.objects.filter(client=client).order_by('-timestamp')[:5]

    context = {
        "client": client,
        "total_conversations": total_conversations,
        "last_messages": last_messages,
    }

    return render(request, "dashboard/home.html", context)
