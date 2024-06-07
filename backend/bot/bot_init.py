from django.conf import settings
from telegram.ext import Application, CommandHandler

from bot.handlers import ads, conv_handler, filter_ad_category, start


def telegram_application():
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ads", ads))
    application.add_handler(CommandHandler(
        "filter_ad_category", filter_ad_category
    ))
    application.add_handler(conv_handler)
    return application


APPLICATION = telegram_application()
