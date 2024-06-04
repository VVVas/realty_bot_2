from django.contrib import admin
from .models import BotMessage


@admin.register(BotMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'keyword', 'text')
