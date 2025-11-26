from django.urls import path
from . import views, webhook

urlpatterns = [
    path('', views.conversations_list, name='conversations_list'),
    path('webhook/', webhook.receive_message, name='webhook_receive'),
]
