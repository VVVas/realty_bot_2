from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import BotMessage
from .resources import BotMessageResource


@admin.register(BotMessage)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ('title', 'keyword', 'text')
    resource_class = BotMessageResource
    # readonly_fields = ('keyword',)
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['keyword']
        else:
            return []
