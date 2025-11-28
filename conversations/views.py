from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Client
from .models import Conversation, Contact
from django.http import JsonResponse
from bot.wpp_api import WPPConnectAPI 
from django.utils.timezone import localtime
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import send_whatsapp_message


@login_required
def conversations_list(request):
    client = Client.objects.get(user=request.user)
    conv = Conversation.objects.filter(client=client).order_by("-timestamp")

    return render(request, "conversations/list.html", {"conversations": conv})


@login_required
def inbox(request):
    client = Client.objects.get(user=request.user)

    # contatos deste client
    contatos = Contact.objects.filter(client=client)

    lista = []

    for c in contatos:

        # última mensagem desse contato
        last_msg = Conversation.objects.filter(
            client=client,
            contato=c
        ).order_by("-timestamp").first()

        lista.append({
            "contato": c,
            "last_msg": last_msg,
        })

    return render(request, "conversations/inbox.html", {
        "lista": lista
    })



@login_required
def chat_detail(request, phone):
    client = Client.objects.get(user=request.user)
    
    # Marca como lidas as mensagens 'naõ lidas'
    Conversation.objects.filter(
        client=client,
        sender=phone,
        is_from_bot=False,
        is_read=False,
    ).update(is_read=True)

    messages = Conversation.objects.filter(
        client=client, sender=phone
    ).order_by("timestamp")

    return render(request, "conversations/chat.html", {
        "phone": phone,
        "messages": messages,
    })


@login_required
def send_message(request, phone):
    client = Client.objects.get(user=request.user)

    if request.method == "POST":
        text = request.POST.get("message")

        # Envia para o WhatsApp Cloud API
        send_whatsapp_message(phone, text)

        # Salva no banco
        Conversation.objects.create(
            client=client,
            sender=str(client.user),
            message=text,
            direction="outgoing",
            is_from_bot=True
        )

        return redirect("conversation_chat", phone=phone)

@login_required
def ajax_messages(request, phone):
    client = Client.objects.get(user=request.user)  
    
    messages = Conversation.objects.filter(
        client = client,
        sender = phone
    ).order_by("timestamp")
    
    data = []
    
    for msg in messages:
        data.append({
            "message": msg.message,
            "timestamp": localtime(msg.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "is_from_bot": msg.is_from_bot,
        })
        
    return JsonResponse({"messages": data})


@csrf_exempt
def whatsapp_webhook(request):

    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=400)

    data = json.loads(request.body)

    # ------ 1) Identificar telefone ------
    sender = data.get("sender", {})
    telefone = sender.get("id") or data.get("from")

    if telefone:
        telefone = telefone.replace("@c.us", "").replace("+", "")

    # ------ 2) Nome do contato ------
    nome = sender.get("pushname") or "Contato"

    # ------ 3) Foto do perfil (WPPConnect) ------
    foto = (
        sender.get("imgUrl") or
        sender.get("profilePicThumbObj", {}).get("eurl") or
        sender.get("profilePicThumbObj", {}).get("img") or
        sender.get("profilePicThumbObj", {}).get("imgFull")
    )

    # ------ 4) Identificar o client dono do webhook ------
    try:
        api_key = request.headers.get("X-Api-Key")
        client = Client.objects.get(bot_api_key=api_key)
    except:
        return JsonResponse({"error": "Client não encontrado"}, status=404)

    # ------ 5) Criar ou atualizar contato ------
    contato, created = Contact.objects.get_or_create(
        client=client,
        telefone=telefone,
        defaults={
            "nome": nome,
            "foto_url": foto
        }
    )

    # se já existe, atualiza a foto se mudou
    if foto and contato.foto_url != foto:
        contato.foto_url = foto
        contato.save()

    # ------ 6) Pegar mensagem recebida ------
    mensagem = data.get("body") or data.get("message") or ""

    # ------ 7) Criar Conversation (ainda sem vínculo ao Contact) ------
    Conversation.objects.create(
        client=client,
        contato=contato,
        sender=telefone,
        message=mensagem,
        message_type="text",
        direction="incoming",
    )

    return JsonResponse({"status": "ok"})
