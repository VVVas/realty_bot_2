import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from bot.bot_init import APPLICATION

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN


class Command(BaseCommand):
    help = 'Устанавливает вебхук для Телеграмм бота'

    async def run_bot(self, url):
        await APPLICATION.bot.set_webhook(url=url)
        async with APPLICATION:
            await APPLICATION.start()
            await APPLICATION.stop()

    def handle(self, *arg, **kwarg):
        url = "{}{}".format(
            settings.GENERAL_URL, reverse("webhook")
        )
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_bot(url))
        if loop:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully set webhook: {url}')
            )
        else:
            self.stdout.write(self.style.ERROR(
                f'Failed to set webhook: {url}')
            )
