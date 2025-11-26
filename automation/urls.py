from django.urls import path
from . import views


urlpatterns = [
    path('settings/', views.automation_settings, name='automation_settings'),
]
