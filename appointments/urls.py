from django.urls import path
from . import views

urlpatterns = [
    path('', views.appointments_list, name='appointments_list'),
    path('novo/', views.appointment_create, name='appointment_create'),
    path('editar/<int:id>/', views.appointment_edit, name='appointment_edit'),
    path('calendar/', views.calendar_view, name='appointments_calendar'),
    path('events/', views.appointments_json, name='appointments_json'),

    # NOVOS ENDPOINTS PARA FULLCALENDAR
    path('event/<int:id>/', views.event_details, name='event_details'),
    path('event/<int:id>/update/', views.event_update, name='event_update'),
    path('event/<int:id>/delete/', views.event_delete, name='event_delete'),
    
]
