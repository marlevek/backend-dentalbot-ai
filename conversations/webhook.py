from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import json
from accounts.models import Client
from .models import Contact
from conversations.models import Conversation


VERIFY_TOKEN = "coderte_webhook_2025"

def receive_webhook(request):
    if request.method == "GET":
        if request.GET.get("hub.mode") == "subscribe" and \
           request.GET.get("hub.verify_token") == VERIFY_TOKEN:
            return HttpResponse(request.GET["hub.challenge"])
        return HttpResponse("Token inválido")

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        try:
            entry = data["entry"][0]["changes"][0]["value"]
            messages = entry.get("messages", [])

            if messages:
                msg = messages[0]
                phone = msg["from"]
                text = msg["text"]["body"]

                client = Client.objects.first()  # ajustar se multi-clínica
                contact, _ = Contact.objects.get_or_create(
                    client=client,
                    phone=phone
                )

                Conversation.objects.create(
                    client=client,
                    contato=contact,
                    sender=phone,
                    message=text,
                    direction="incoming"
                )

        except Exception as e:
            print("Erro no webhook:", e)

        return HttpResponse("EVENT_RECEIVED")


@csrf_exempt
def receive_message(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    # ============================
    # 1. API KEY
    # ============================
    api_key = request.GET.get("api_key")

    try:
        client = Client.objects.get(api_key=api_key)
    except Client.DoesNotExist:
        return JsonResponse({"error": "Invalid API Key"}, status=400)

    # ============================
    # 2. JSON recebido
    # ============================
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Exemplo de payload do WPPConnect
    sender = data.get("from", {}).get("remoteJid", "")
    msg_text = data.get("text") or data.get("body") or ""

    # ============================
    # 3. Detecta se é mensagem do BOT
    # ============================
    # WPPConnect envia mensagens do bot com this.isMe == true
    is_from_bot = str(data.get("from", {}).get("isMe", False)).lower() == "true"

    # ============================
    # 4. Reset mensal
    # ============================
    client.reset_monthly_limit_if_needed()

    # ============================
    # 5. Controle de limite (exceto mensagens do bot)
    # ============================
    plan = client.plan

    is_unlimited = (
        plan.max_conversations is None or
        plan.max_conversations == 0
    )

    if not is_unlimited and not is_from_bot:
        if client.conversations_used >= plan.max_conversations:
            # Mesmo sem contar, salvamos no histórico
            Conversation.objects.create(
                client=client,
                sender=sender,
                message=msg_text,
                direction="incoming",
                is_from_bot=is_from_bot
            )
            return JsonResponse({"status": "limit_reached"})

    # ============================
    # 6. Salva no banco
    # ============================
    Conversation.objects.create(
        client=client,
        sender=sender,
        message=msg_text,
        direction="incoming" if not is_from_bot else "outgoing",
        is_from_bot=is_from_bot
    )

    # ============================
    # 7. Incrementa limite
    # ============================
    if not is_unlimited and not is_from_bot:
        client.conversations_used += 1
        client.save()

    # ============================
    # 8. Aviso de 80%
    # ============================
    if not is_unlimited:
        if client.conversations_used >= int(plan.max_conversations * 0.8):
            client.alert_upgrade = True
            client.save()

    return JsonResponse({"status": "received"})
