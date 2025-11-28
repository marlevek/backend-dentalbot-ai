
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Client
from .models import Appointment
import datetime
from django.http import JsonResponse


@login_required
@login_required
def appointments_list(request):

    # pega o client correto vinculado ao usuário logado
    client = Client.objects.get(user=request.user)

    # lista apenas os agendamentos do client logado
    agendamentos = Appointment.objects.filter(client=client).order_by("data", "hora")

    # mesmo mapa do calendário
    icon_map = {
        "Implante": "/static/img/procedures/implante.png",
        "Exodontia": "/static/img/procedures/exodontia.png",
        "Profilaxia": "/static/img/procedures/profilaxia.png",
        "Ortodontia": "/static/img/procedures/ortodontia.png",
        "Avaliação": "/static/img/procedures/avaliacao.png",
        "Clareamento": "/static/img/procedures/clareamento.png",
        "Endodontia": "/static/img/procedures/endodontia.png",
        "Restauração": "/static/img/procedures/restauracao.png",
    }

    # adiciona atributo .icon em cada agendamento para usar na listagem
    for a in agendamentos:
        a.icon = icon_map.get(a.procedimento, "/static/img/procedures/default.png")

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


@login_required
def calendar_view(request):
    return render(request, "appointments/calendar.html")


@login_required
def appointments_json(request):
    client = Client.objects.get(user=request.user)
    agendamentos = Appointment.objects.filter(client=client)

    icon_map = {
    "Implante": "/static/img/procedures/implante.png",
    "Exodontia": "/static/img/procedures/exodontia.png",
    "Profilaxia": "/static/img/procedures/profilaxia.png",
    "Ortodontia": "/static/img/procedures/ortodontia.png",
    "Avaliação": "/static/img/procedures/avaliacao.png",
    "Clareamento": "/static/img/procedures/clareamento.png",
    "Endodontia": "/static/img/procedures/endodontia.png",
    "Restauração": "/static/img/procedures/restauracao.png",
}


    colors = {
        "Clareamento": "#4dabf7",
        "Avaliação": "#82c91e",
        "Implante": "#ff922b",
        "Ortodontia": "#9775fa",
        "Limpeza": "#15aabf",
        "Urgência": "#fa5252",
    }

    events = []

    for a in agendamentos:
        icon_url = icon_map.get(a.procedimento, "")
        
         # HTML DA IMAGEM
        icon_html = ""
        if icon_url:
            icon_html = (
                f"<img src='{icon_url}' "
                f"style='height:18px; width:18px; margin-right:6px; "
                f"object-fit:contain; vertical-align:middle;'>"
            )
        
        # TÍTULO FINAL
        title_html = f"{icon_html}{a.paciente} — {a.procedimento}"

        events.append({
            "id": a.id,
            "title": f"{a.paciente} — {a.procedimento}",
            "start": f"{a.data}T{a.hora}",
            "color": colors.get(a.procedimento, "#4c6ef5"),
            "icon": icon_url,  # <<<<<<<<<< ADICIONAR ISSO
        })
        
    return JsonResponse(events, safe=False)

# DETALHES DO EVENTO
@login_required
def event_details(request, id):
    client = Client.objects.get(user=request.user)
    try:
        a = Appointment.objects.get(id=id, client=client)
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    return JsonResponse({
        "id": a.id,
        "paciente": a.paciente,
        "telefone": a.telefone,
        "procedimento": a.procedimento,
        "data": str(a.data),
        "hora": str(a.hora),
        "status": a.status,
        "obs": a.obs or ""
    })


@login_required
def event_update(request, id):
    client = Client.objects.get(user=request.user)
    try:
        a = Appointment.objects.get(id=id, client=client)
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    if request.method == "POST":
        a.data = request.POST.get("data")
        a.hora = request.POST.get("hora")
        a.paciente = request.POST.get("paciente")
        a.telefone = request.POST.get("telefone")
        a.procedimento = request.POST.get("procedimento")
        a.status = request.POST.get("status")
        a.obs = request.POST.get("obs")
        a.save()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "invalid"}, status=400)


@login_required
def event_delete(request, id):
    client = Client.objects.get(user=request.user)
    try:
        a = Appointment.objects.get(id=id, client=client)
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)

    a.delete()
    return JsonResponse({"success": True})


@login_required
def appointment_edit(request, id):
    client = Client.objects.get(user=request.user)

    try:
        a = Appointment.objects.get(id=id, client=client)
    except Appointment.DoesNotExist:
        return redirect("appointments_list")

    if request.method == "POST":
        a.paciente = request.POST.get("paciente")
        a.telefone = request.POST.get("telefone")
        a.procedimento = request.POST.get("procedimento")
        a.data = request.POST.get("data")
        a.hora = request.POST.get("hora")
        a.status = request.POST.get("status")
        a.obs = request.POST.get("obs")
        a.save()

        return redirect("appointments_list")

    return render(request, "appointments/edit.html", {"a": a})
