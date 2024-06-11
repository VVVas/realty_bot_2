import datetime
from sys import stdout

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          filters, MessageHandler,)

from realties.models import City, Category # noqa

START, CITY, CITY_CHOICE, CATEGORY = range(4)


def stdout_message(update):
    return stdout.write(f"{datetime.datetime.now()}"
                        f"Бот получил сообщение {update.message.text} "
                        f"от {update.message.from_user.first_name} "
                        f"{update.message.from_user.last_name}\n")


async def start(update: Update, context: CallbackContext) -> int:
    greeting_message = (
        'Тут будет приветствие. \n'
        'Выберите действие открыв клавиатуру \n'
        'Или нажав на кнопку в компьютерной версии.'
    )
    stdout_message(update)
    keyboard = [['Начало работы', 'О боте']]

    await update.message.reply_text(
        greeting_message,
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )

    return START


async def help_command(update: Update, context: CallbackContext) -> int:
    bot_description = 'Тут будет описание работы'
    stdout_message(update)
    await update.message.reply_text(bot_description)
    return START


async def start_work(update: Update, context: CallbackContext) -> int:
    stdout_message(update)
    await update.message.reply_text(
        "Давайте начнем поиск объявлений. Пожалуйста, введите название города:"
    )

    return CITY_CHOICE


async def city_choice(update: Update, context: CallbackContext) -> int:
    list_button = [[]]
    city_name = update.message.text
    list_names = [city.name for city in City.objects.all()]
    for city in list_names:
        if city.startswith(city_name):
            list_button[0].append(city)
    stdout_message(update)
    await update.message.reply_text(
        'Вот какие города я нашёл. Выберите нужный из списка:',
        reply_markup=ReplyKeyboardMarkup(
            list_button,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return CITY


async def select_city(update: Update, context: CallbackContext) -> int:
    list_button = [[]]
    list_names = [city.title for city in Category.objects.all()]
    for city in list_names:
        list_button[0].append(city)
    stdout_message(update)
    selected_city = update.message.text
    context.user_data['selected_city'] = selected_city
    await update.message.reply_text(
        'Отлично! Теперь необходимо выбрать категорию',
        reply_markup=ReplyKeyboardMarkup(
            list_button,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )

    return CATEGORY


async def select_category(update: Update, context: CallbackContext) -> int:
    stdout_message(update)
    selected_category = update.message.text
    context.user_data['selected_category'] = selected_category
    await update.message.reply_text(
        f"Отлично! "
        f"Вот параметры выборки, который вы выбрали: \n"
        f"Город: {context.user_data['selected_city']}\n"
        f"Категория: {context.user_data['selected_category']}\n"
        f"Выборку сделаю когда будет список объявлений\n"
        f"Ad.objects.filter(тут параметры)"
    )
    context.user_data.clear()
    return ConversationHandler.END


search_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START: [
            MessageHandler(filters.Regex('^(О боте)$'), help_command),
            MessageHandler(filters.Regex('^(Начало работы)$'), start_work)
        ],
        CITY_CHOICE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, city_choice)
        ],
        CITY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, select_city)
        ],
        CATEGORY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, select_category)
        ],
        # PRICE: [
        #     MessageHandler(Filters.text & ~Filters.command, select_price)],
    },
    fallbacks=[],
)
