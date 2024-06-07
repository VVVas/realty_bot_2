from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from telegram import Bot
import asyncio

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
WEBHOOK_URL = 'https://pb.vvvas.ru/webhook/'


class Command(BaseCommand):
    help = 'Устанавливает вебхук для Телеграмм бота'

    def handle(self, *arg, **kwarg):
        bot = Bot(token=TELEGRAM_TOKEN)
        url = "{}{}".format(
            settings.GENERAL_URL, reverse("webhook")
        )
        response = asyncio.run(self.set_webhook(bot, url))
        if response:
            self.stdout.write(self.style.SUCCESS(
                f'Successfully set webhook: {WEBHOOK_URL}')
            )
        else:
            self.stdout.write(self.style.ERROR(
                f'Failed to set webhook: {WEBHOOK_URL}')
            )


    async def set_webhook(self, bot, url):
        return await bot.set_webhook(url=url)
