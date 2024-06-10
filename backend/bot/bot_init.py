from django.conf import settings
from telegram.ext import Application

from .handlers2 import (CommandHandler, ads, conv_handler,
                        filter_ad_category, start)


class TGBot:
    def __init__(self):
        self.ptb_app = (
            Application
            .builder()
            .token(settings.TELEGRAM_TOKEN)
            .updater(None)
            .build()
        )
        self.ptb_app.add_handler(CommandHandler("start", start))
        self.ptb_app.add_handler(CommandHandler("ads", ads))
        self.ptb_app.add_handler(CommandHandler(
            "filter_ad_category", filter_ad_category
        ))
        self.ptb_app.add_handler(conv_handler)


# def telegram_application():
#     application = (
#         Application
#         .builder()
#         .token(settings.TELEGRAM_TOKEN)
#         .updater(None)
#         .build()
#     )
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("ads", ads))
#     application.add_handler(CommandHandler(
#         "filter_ad_category", filter_ad_category
#     ))
#     application.add_handler(conv_handler)
#     return application
#
#
# APPLICATION = telegram_application()
tgbot = TGBot()
