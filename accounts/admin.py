from django.contrib import admin
from .models import Client, Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "max_conversations", "price_month")
    search_fields = ("name",)
    
    def max_conversations(self, obj):
        if obj.max_conversations is [None, 0]:
            return "Ilimitado"
        return obj.max_conversations


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("clinic_name", "user", "plan", "status")
    search_fields = ("clinic_name", "user__username")
    list_filter = ("plan", "status")


