
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import uuid


# ------------------------------
# Função correta para default
# ------------------------------
def default_trial_expiration():
    return datetime.now() + timedelta(days=7)


class Plan(models.Model):
    name = models.CharField(max_length=50)
    max_conversations = models.IntegerField(default=200)
    price_month = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='trial'
    )

    trial_expires_at = models.DateTimeField(default=default_trial_expiration)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_trial_active(self):
        return self.status == 'trial' and datetime.now() < self.trial_expires_at

    def __str__(self):
        return self.clinic_name
