from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for start command"""
    text = 'Welcome to webhook bot'
    await update.message.reply_html(text=text)
