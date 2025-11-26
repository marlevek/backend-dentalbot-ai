from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Client, Plan




def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("dashboard_home")
        messages.error(request, "Credenciais inválidas.")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        clinic_name = request.POST.get("clinic_name")

        user = User.objects.create_user(username=username, password=password)

        # Plano Starter (trial)
        starter_plan = Plan.objects.filter(name="Starter").first()

        Client.objects.create(
            user=user,
            clinic_name=clinic_name,
            plan=starter_plan
        )

        messages.success(request, "Conta criada com sucesso!")
        return redirect("login")

    return render(request, "accounts/register.html")


@login_required
def plan_view(request):
    client = Client.objects.get(user=request.user)
    return render(request, "accounts/plan.html", {"client": client})

