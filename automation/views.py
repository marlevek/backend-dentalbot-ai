from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Client
from .models import AutoReplyConfig


@login_required
def automation_settings(request):
    client = Client.objects.get(user=request.user)
    config, created = AutoReplyConfig.objects.get_or_create(client=client)

    if request.method == "POST":
        config.welcome_message = request.POST.get("welcome_message")
        config.out_of_hours_message = request.POST.get("out_of_hours_message")
        config.working_start = request.POST.get("working_start")
        config.working_end = request.POST.get("working_end")

        config.faq_clareamento = request.POST.get("faq_clareamento")
        config.faq_implante = request.POST.get("faq_implante")
        config.faq_aparelho = request.POST.get("faq_aparelho")
        config.faq_orcamento = request.POST.get("faq_orcamento")

        config.save()

    return render(request, "automation/settings.html", {"config": config})
