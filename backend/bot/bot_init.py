from django.conf import settings
from telegram.ext import Application

from .handlers import comment
from .handlers.search import search_conv_handler
from .handlers.favorite import favorite_handler, delete_favorite_handler
from .handlers.unknown import unknown_message


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
        self.ptb_app.add_handler(favorite_handler)
        self.ptb_app.add_handler(delete_favorite_handler)
        self.ptb_app.add_handler(comment.add_conv)
        self.ptb_app.add_handler(unknown_message)


tgbot = TGBot()
