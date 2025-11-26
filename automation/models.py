from django.db import models
from accounts.models import Client 


class AutoReplyConfig(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    welcome_message = models.TextField(default="Olá! Sou a assistente virtual da clínica. Como posso ajudar?")
    out_of_hours_message = models.TextField(default="Estamos fora do horário de atendimento. Responderemos assim que possível.")

    working_start = models.TimeField(default="08:00")
    working_end = models.TimeField(default="18:00")

    faq_clareamento = models.TextField(blank=True, null=True)
    faq_implante = models.TextField(blank=True, null=True)
    faq_aparelho = models.TextField(blank=True, null=True)
    faq_orcamento = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Atendimento Automático — {self.client.clinic_name}"



