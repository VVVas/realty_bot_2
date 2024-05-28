from django.conf import settings
from telegram import Bot
from telegram.ext import Dispatcher

from .handlers import handler


def telegram_bot():
    bot = Bot(settings.TOKEN_BOT)
    return bot


def telegram_dispatcher():
    bot = telegram_bot()
    dispatcher = Dispatcher(bot, None, workers=0)
    dispatcher.add_handler(handler)

    return dispatcher


BOT = telegram_bot()
DISPATCHER = telegram_dispatcher()
