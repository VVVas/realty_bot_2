from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from bot.bot_init import APPLICATION


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = "{}{}".format(settings.GENERAL_URL, reverse("process"))
        is_appointed = APPLICATION.bot.set_webhook(url=url)
        if is_appointed:
            self.stdout.write(self.style.SUCCESS(
                "Webhook was successfully appointed."
            ))
        else:
            self.stdout.write(self.style.ERROR("Something went wrong."))
