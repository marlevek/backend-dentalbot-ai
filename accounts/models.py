
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import uuid
from django.utils.timezone import now

# ------------------------------
# Função correta para default
# ------------------------------
def default_trial_expiration():
    return datetime.now() + timedelta(days=7)


class Plan(models.Model):
    name = models.CharField(max_length=50)
    price_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Limite de conversas — None = ilimitado
    max_conversations = models.IntegerField(
        null=True,
        blank=True,
        help_text="Deixe vazio para conversas ilimitadas."
    )

    description = models.TextField(blank=True, null=True)

    def is_unlimited(self):
        return self.max_conversations is None

    def __str__(self):
        if self.is_unlimited():
            return f"{self.name} (Ilimitado)"
        return f"{self.name} ({self.max_conversations} conversas/mês)"


class Client(models.Model):
    STATUS_CHOICES = (
        ('trial', 'Em teste'),
        ('active', 'Ativo'),
        ('suspended', 'Suspenso'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic_name = models.CharField(max_length=150)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    api_key = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    conversations_used = models.IntegerField(default=0)
    month_cycle = models.DateField(default=datetime.now)
    alert_upgrade = models.BooleanField(default=False)
    
    
    def reset_monthly_limit_if_needed(self):
        today = datetime.now().date()
        
        if self.month_cycle != today.day:
            self.converations_used = 0
            self.month_cycle = today
            self.alert_upgrade = False
            self.save()
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='trial'
    )

    def is_over_limit(self):
        plan = self.plan
        if plan.max_conversations in [None, 0]:  # ilimitado
            return False
        return self.conversations_used >= plan.max_conversations
    
    
    def usage_percentage(self):
        plan = self.plan
        if plan is None:
            return 0
        if plan.max_conversations in [None, 0]:
            return 0
        return int((self.conversations_used / plan.max_conversations) * 100)
    

    trial_expires_at = models.DateTimeField(default=default_trial_expiration)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_trial_active(self):
        return self.status == 'trial' and datetime.now() < self.trial_expires_at

    def __str__(self):
        return self.clinic_name

  