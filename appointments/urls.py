from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointments_list, name='appointments_list'),
    path('novo/', views.appointment_create, name='appointment_create'),
]
