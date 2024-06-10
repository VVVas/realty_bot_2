from django.conf import settings
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from tg_bot.handlers import start_handler, echo_handler


class TGBot:
    def __init__(self):
        self.ptb_app = (
            Application.builder()
            .token(settings.TELEGRAM_TOKEN)  # Set TOKEN value
            .updater(None)
            .build()
        )
        self.ptb_app.add_handler(CommandHandler("start", start_handler.start))
        self.ptb_app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler.echo)
        )


tgbot = TGBot()
