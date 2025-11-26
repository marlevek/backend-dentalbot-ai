from django.db import models
from accounts.models import Client

PROCEDIMENTOS = [
    ("Clareamento", "Clareamento"),
    ("Avaliação", "Avaliação"),
    ("Implante", "Implante"),
    ("Ortodontia", "Ortodontia"),
    ("Limpeza", "Limpeza"),
    ("Urgência", "Urgência"),
]

STATUS = [
    ("Pendente", "Pendente"),
    ("Confirmado", "Confirmado"),
    ("Concluído", "Concluído"),
    ("Cancelado", "Cancelado"),
]


class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    paciente = models.CharField(max_length=120)
    telefone = models.CharField(max_length=20)
    procedimento = models.CharField(max_length=50, choices=PROCEDIMENTOS)
    data = models.DateField()
    hora = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS, default="Pendente")
    obs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.paciente} — {self.procedimento}"
