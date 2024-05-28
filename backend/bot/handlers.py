from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)


HELLO, INFO, WORK = range(3)


def start(update: Update, _: CallbackContext):
    reply_keyboard = [['Информация о боте', 'Начать поиск недвижимости']]
    update.message.reply_text(
        'Добро пожаловать в доб по поиску недвижимости! '
        'Сейчас вы можете получить информацию о работе с ботом.'
        'Или сразу начать поиск недвижимости',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )

    return HELLO


def info(update: Update, _: CallbackContext):
    update.message.reply_text(
        'Здесь какой-то текст о работе бота.'
        'Потом добавлю модуль в приложение, чтобы можно было из админки менять'
    )

    return ConversationHandler.END


def work(update: Update, _: CallbackContext):
    update.message.reply_text(
        'Здесь будет логика работы бота, но позже'
    )


def cancel(update: Update, _: CallbackContext):
    update.message.reply_text(
        'Отмена. Надеемся увидеть Вас снова!'
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
