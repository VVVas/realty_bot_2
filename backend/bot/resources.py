from import_export import resources

from .models import BotMessage


class BotMessageResource(resources.ModelResource):

    def skip_row(self, instance, original,
                 row, import_validation_errors=None):
        if BotMessage.objects.filter(keyword=row['keyword']):
            return True
        else:
            return False


    class Meta:
        model = BotMessage
