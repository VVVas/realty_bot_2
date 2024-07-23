from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, filters


async def handle_unknown_messages(update: Update, context: CallbackContext) -> None:
    context.user_data.clear()
    if not update.message.text.startswith('/'):
        return await update.message.reply_text(
            'Для продолжения работы необходимо вызвать функцию /start'
        )

    return None

unknown_message = MessageHandler(
    filters.TEXT & ~filters.COMMAND, handle_unknown_messages
)
