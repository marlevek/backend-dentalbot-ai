from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation
from accounts.models import Client
import json


@csrf_exempt
def receive_message(request):
    if request.method == "POST":

        # API Key usada como segurança
        client_api_key = request.GET.get("api_key")

        try:
            client = Client.objects.get(api_key=client_api_key)
        except Client.DoesNotExist:
            return JsonResponse({"error": "Invalid API Key"}, status=400)

        data = json.loads(request.body.decode("utf-8"))

        sender = data.get("from", {}).get("remoteJid", "")
        msg_text = data.get("text", "")

        if not msg_text:
            msg_text = data.get("body", "")  # fallback

        # Salva no banco
        Conversation.objects.create(
            client=client,
            sender=sender,
            message=msg_text,
            direction="incoming"
        )

        return JsonResponse({"status": "received"})

    return JsonResponse({"error": "Invalid method"}, status=405)
