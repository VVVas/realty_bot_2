from django.conf import settings
from telegram.ext import Application

from .handlers import handler


def telegram_application():
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(handler)
    return application


APPLICATION = telegram_application()
