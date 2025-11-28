from django.urls import path
from . import views, webhook

urlpatterns = [
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

    # 🔹 WEBHOOK
    path("webhook/", webhook.receive_webhook)
]
