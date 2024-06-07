import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from bot.bot_init import APPLICATION

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN


class Command(BaseCommand):
    help = 'Устанавливает вебхук для Телеграмм бота'

    def handle(self, *arg, **kwarg):
        url = "{}{}".format(
            settings.GENERAL_URL, reverse("webhook")
        )
        response = asyncio.run(self.set_webhook(url))
        if response:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully set webhook: {url}')
            )
        else:
            self.stdout.write(self.style.ERROR(
                f'Failed to set webhook: {url}')
            )

    async def set_webhook(self, url):
        return await APPLICATION.bot.set_webhook(url=url)
