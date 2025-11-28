from django.urls import path
from . import views, webhook
from .webhook import whatsapp_webhook



urlpatterns = [
    # 🔹 Webhook oficial do WhatsApp Cloud API
    path('webhook/', whatsapp_webhook, name='whatsapp_webhook'),
    
    # 🔹 INBOX precisa vir ANTES do <phone>
    path("inbox/", views.inbox, name="inbox"),

    # 🔹 LISTA GERAL
    path("", views.conversations_list, name="conversations_list"),

    # 🔹 CHAT DETALHADO
    path("<str:phone>/", views.chat_detail, name="conversation_chat"),

    # 🔹 ENVIAR
    path("<str:phone>/send/", views.send_message, name="conversation_send"),

    # 🔹 AJAX MESSAGES
    path("<str:phone>/messages/", views.ajax_messages, name="conversation_messages_ajax"),

]
