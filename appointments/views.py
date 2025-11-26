
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Client
from .models import Appointment


@login_required
def appointments_list(request):
    client = Client.objects.get(user=request.user)

    agendamentos = Appointment.objects.filter(client=client).order_by("data", "hora")

    return render(request, "appointments/list.html", {
        "agendamentos": agendamentos
    })


@login_required
def appointment_create(request):
    client = Client.objects.get(user=request.user)

    if request.method == "POST":
        Appointment.objects.create(
            client=client,
            paciente=request.POST.get("paciente"),
            telefone=request.POST.get("telefone"),
            procedimento=request.POST.get("procedimento"),
            data=request.POST.get("data"),
            hora=request.POST.get("hora"),
            status="Pendente",
            obs=request.POST.get("obs")
        )
        return redirect("appointments_list")

    return render(request, "appointments/create.html")
