from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

TELEGRAM_TOKEN = 'value'
GREETINGS = ("привет, {name}. "
             "Это бот, который создает единое пространство по предоставлению "
             "информации о коммерческих площадках и их собственниках, "
             "для облегчения поиска предпринимателям.")


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='hi')


def start(update, context):
    chat = update.effective_chat
    markup = ReplyKeyboardMarkup([['/help']])
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'{GREETINGS.format(name = chat.first_name)}'),
        reply_markup=markup
    )


def help(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text='help,')
    update.message.reply_text('some settings')


updater = Updater(token=TELEGRAM_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('help', help))
dp.add_handler(MessageHandler(Filters.text, say_hi))
updater.start_polling()
updater.idle()
