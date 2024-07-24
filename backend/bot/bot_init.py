from django.conf import settings
from telegram.ext import Application

from .handlers import comment, favorite, unknown
from .handlers.search import search_conv_handler


class TGBot:
    def __init__(self):
        """Создаём бота и добавляем в него обработчики сообщений."""
        self.ptb_app = (
            Application
            .builder()
            .token(settings.TELEGRAM_TOKEN)
            .updater(None)
            .build()
        )
        self.ptb_app.add_handler(search_conv_handler)
        self.ptb_app.add_handler(comment.handler)
        self.ptb_app.add_handler(comment.add_conv)
        self.ptb_app.add_handler(favorite.add_handler)
        self.ptb_app.add_handler(favorite.delete_handler)
        self.ptb_app.add_handler(unknown.handler)


tgbot = TGBot()
