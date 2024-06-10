from django.conf import settings
from telegram.ext import Application, CommandHandler


from .handlers2 import ads, conv_handler, filter_ad_category, start


class TGBot:
    def __init__(self):
        """Создаём бота и добавляем в него обработчики сообщений"""
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


tgbot = TGBot()
