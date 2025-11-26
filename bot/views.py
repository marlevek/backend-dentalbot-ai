from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Client
from .models import BotConfig
from .services import WPPConnectAPI



@login_required
def bot_config_view(request):
    client = Client.objects.get(user=request.user)
    config, created = BotConfig.objects.get_or_create(client=client)
    
    api = WPPConnectAPI(client)
    
    if request.method == "POST":
        config.sessinon_name = request.POST.get("session_name")
        config.instance_url = request.POST.get("instance_url")
        config.save()
        
        # atualiza status e QR
        api.get_status()
        api.get_qr_code()

    return render(request, "bot/config.html", {"config": config})
