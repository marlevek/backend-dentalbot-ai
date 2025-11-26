from django.urls import path
from . import views

urlpatterns = [
    path('config/', views.bot_config_view, name='bot_config'),
]
