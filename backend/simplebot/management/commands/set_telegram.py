from django.conf import settings
from django.core.management import BaseCommand
from django.urls import reverse
from telegram import Update

from simplebot.views import ptb_application


class Command(BaseCommand):
    help = "Set new telegram webhook"

    def handle(self, *arg, **kwarg):
        webhook_path = reverse('simplebot:ptb')
        webhook_url = f'{settings.GENERAL_URL}/{webhook_path}'

        print(webhook_url)

        # ptb_application.bot.set_webhook(
        #     url=webhook_url,
        #     allowed_updates=Update.ALL_TYPES
        # )
