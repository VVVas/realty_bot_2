from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackContext,
)

from .models import BotMessage

HELLO, INFO, WORK = range(3)


async def start(update: Update, _: CallbackContext):
    reply_keyboard = [['Информация о боте', 'Начать поиск недвижимости']]
    await update.message.reply_text(
        Message.objects.filter(keyword='START')[0].text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )

    return HELLO


async def info(update: Update, _: CallbackContext):
    await update.message.reply_text(
        Message.objects.filter(keyword='HELP')[0].text
    )

    return ConversationHandler.END


async def work(update: Update, _: CallbackContext):
    await update.message.reply_text(
        'Здесь будет логика работы бота, но позже'
    )


async def cancel(update: Update, _: CallbackContext):
    await update.message.reply_text(
        Message.objects.filter(keyword='CANCEL')[0].text
    )
    return ConversationHandler.END


handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        INFO: [CommandHandler('info', info)],
        WORK: [CommandHandler('work', work)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
