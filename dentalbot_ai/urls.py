from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import test_message



def home_redirect(request):
    return redirect("/dashboard/")


urlpatterns = [
     path("test-message/", test_message, name="test_message"),
    
    path("", home_redirect),  # ⬅️ redirecionamento automático
    path('admin/', admin.site.urls),
    
    # Apps principais 
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('bot/', include('bot.urls')),
    path("conversations/", include("conversations.urls")),
    path('automation/', include('automation.urls')),
    path('appointments/', include('appointments.urls')),    
   
]
