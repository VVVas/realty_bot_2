import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from telegram import Update

from bot.bot_init import tgbot


TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN


class Command(BaseCommand):
    help = 'Устанавливает вебхук для Телеграмм бота'

    async def run_bot(self):
        url = "{}{}".format(settings.GENERAL_URL, reverse('webhook'))
        await tgbot.ptb_app.bot.set_webhook(
            url=url,
            allowed_updates=Update.ALL_TYPES
        )
        async with tgbot.ptb_app:
            await tgbot.ptb_app.start()
            await tgbot.ptb_app.stop()

    def handle(self, *args, **options):

        try:
            # asyncio.get_event_loop().run_until_complete(self.run_bot())
            self.stdout.write(self.style.SUCCESS("Бот запущен"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Something went wrong. {e}"))
