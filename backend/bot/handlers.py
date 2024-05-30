from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

from .models import BotMessage


HELLO, INFO, WORK = range(3)


def start(update: Update, _: CallbackContext):
    reply_keyboard = [['Информация о боте', 'Начать поиск недвижимости']]
    update.message.reply_text(
        BotMessage.objects.filter(keyword='START')[0].text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )

    return HELLO


def info(update: Update, _: CallbackContext):
    update.message.reply_text(
        BotMessage.objects.filter(keyword='HELP')[0].text
    )

    return ConversationHandler.END


def work(update: Update, _: CallbackContext):
    update.message.reply_text(
        'Здесь будет логика работы бота, но позже'
    )


def cancel(update: Update, _: CallbackContext):
    update.message.reply_text(
        BotMessage.objects.filter(keyword='CANCEL')[0].text
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
