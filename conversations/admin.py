from django.contrib import admin
from .models import Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("client", "sender", "message", "timestamp", "is_from_bot", "is_read")
    list_filter = ("is_from_bot", "is_read")
    search_fields = ("sender", "message")
