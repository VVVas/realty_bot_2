from import_export import resources
from .models import BotMessage


class BotMessageResource(resources.ModelResource):
    class Meta:
        model = BotMessage
