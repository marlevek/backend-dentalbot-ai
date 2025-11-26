from django.db import models
from accounts.models import Client 


class BotConfig(models.Model):
    STATUS_CHOICES = (
        ('offline', 'Offline'),
        ('online', 'Online'),   
        ('loading', 'Loading')
    )
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    
    # Informações de conexão com o WPPConnect 
    sessinon_name = models.CharField(max_length=100, default='dentalbot_session')
    instance_url = models.URLField(
        default='https:localhost:21465',
        help_text='URL da instância do WPPConnect'
    )

    whatsapp_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Número conectado à sessão'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='offline',
    )
    
    last_sync = models.DateTimeField(blank=True, null=True)
    qr_code = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'BotConfig for {self.client.clinic_name} - Status: {self.status}'