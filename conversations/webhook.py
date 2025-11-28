from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from accounts.models import Client
from .models import Contact
from conversations.models import Conversation

# --- TOKEN DE VERIFICAÇÃO DO FACEBOOK ---
VERIFY_TOKEN = "codertec123"


# ============================================================
# 1. WEBHOOK OFICIAL DO WHATSAPP CLOUD API (GET + POST)
# ============================================================

@csrf_exempt
def whatsapp_webhook(request):
    # ====== GET: validação do Facebook ======
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)

        return HttpResponse("Token inválido", status=403)

    # ====== POST: mensagens reais do WhatsApp ======
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            entry = data["entry"][0]["changes"][0]["value"]
            messages = entry.get("messages", [])

            if messages:
                msg = messages[0]
                phone = msg["from"]
                text = msg["text"]["body"] if "text" in msg else ""

                # Pegamos o único cliente por enquanto
                client = Client.objects.first()

                # Cadastra contato
                contact, _ = Contact.objects.get_or_create(
                    client=client,
                    phone=phone
                )

                # Salva mensagem
                Conversation.objects.create(
                    client=client,
                    contato=contact,
                    sender=phone,
                    message=text,
                    direction="incoming",
                    is_from_bot=False
                )

        except Exception as e:
            print("Erro no webhook WhatsApp:", e)

        return HttpResponse("EVENT_RECEIVED", status=200)

    return HttpResponse(status=405)
