from django.db import models
from accounts.models import Client


class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, blank=True, null=True)
    telefone = models.CharField(max_length=30)
    foto_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome or self.telefone}"


class Conversation(models.Model):
    MESSAGE_TYPE = (
        ('text', 'Texto'),
        ('image', 'Imagem'),
        ('audio', 'Áudio'),
        ('video', 'Vídeo'),
        ('file', 'Arquivo'),
    )

    DIRECTION = (
        ('incoming', 'Recebida'),
        ('outgoing', 'Enviada'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contato = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)

    sender = models.CharField(max_length=100)  # número do WhatsApp
    message = models.TextField(blank=True, null=True)

    message_type = models.CharField(
        max_length=20,
        choices=MESSAGE_TYPE,
        default='text'
    )

    direction = models.CharField(
        max_length=20,
        choices=DIRECTION,
        default='incoming'
    )

    ai_response = models.TextField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    
    is_from_bot = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    status = models.CharField(
        max_length=50,
        default="received",
        help_text="Status da mensagem (delivered, read, etc)"
    )

    def __str__(self):
        return f"{self.sender} — {self.message[:30] if self.message else ''}"


    
    