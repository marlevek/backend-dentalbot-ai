from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Client, Plan
from conversations.models import Conversation

@login_required
def dashboard_home(request):
    client, created = Client.objects.get_or_create(
    user=request.user,
    defaults={
        "clinic_name": request.user.username,
        "plan": Plan.objects.first(),  # Starter por padrão
    }
)

    # Reset mensal automático
    client.reset_monthly_limit_if_needed()

    total_conversations = Conversation.objects.filter(client=client).count()
    last_messages = Conversation.objects.filter(client=client).order_by("-timestamp")[:5]

    plan = client.plan
    
    if plan is None:
        is_unlimited = True
        percent_used = 0
    else:
        is_unlimited = plan.max_conversations in [None, 0]
        percent_used = client.usage_percentage()
    
    context = {
        "client": client,
        "total_conversations": total_conversations,
        "last_messages": last_messages,
        "percent_used": percent_used,
        "is_unlimited": is_unlimited,
    }

    return render(request, "dashboard/home.html", context)
