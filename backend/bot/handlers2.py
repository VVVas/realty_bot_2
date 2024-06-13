from django.db.models import Q
from telegram import (ReplyKeyboardMarkup, Update, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          MessageHandler, filters, CallbackQueryHandler)

from realties.models import Category, City, Ad, Realty
from users.models import Profile
from .utils import get_botmessage_by_keyword, chunks

START, CITY, CITY_CHOICE, CATEGORY, PRICE = range(5)
COMMENT, FAVORITE = range(5, 7)


async def start(update: Update, context: CallbackContext) -> int:
    greeting_message = get_botmessage_by_keyword('WELCOME')
    Profile.objects.get_or_create(
        external_id=update.message.from_user.id,
        username=update.message.from_user.username,
        first_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name
    )
    # if update.message.from_user.id in Profile.objects.all() - другие кнопки
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
    bot_description = get_botmessage_by_keyword('BOT_DESCRIPTION')
    await update.message.reply_text(bot_description)
    return START


async def start_work(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Давайте начнем поиск объявлений. Пожалуйста, введите название города:"
    )

    return CITY_CHOICE


async def city_choice(update: Update, context: CallbackContext) -> int:
    list_button = [[]]
    city_name = update.message.text
    list_names = [city.title for city in City.objects.all()]
    for city in list_names:
        if city.istartswith(city_name):
            list_button[0].append(city)
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
    list_names = [category.title for category in Category.objects.all()]
    chunk_size = 3
    list_chunks = list(chunks(list_names, chunk_size))
    keyboard = [chunk for chunk in list_chunks]
    selected_city = update.message.text
    context.user_data['selected_city'] = selected_city
    await update.message.reply_text(
        'Отлично! Теперь необходимо выбрать категорию',
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True
        )
    )

    return CATEGORY


async def select_category(update: Update, context: CallbackContext) -> int:
    selected_category = update.message.text
    context.user_data['selected_category'] = selected_category
    await update.message.reply_text(
        'Остался последний шаг! Необходимо выбрать ценовой диапозон.\n'
        'Введите его, разделяя цифры тире (-).\n'
        'Например: 10000-20000'
    )

    return PRICE


async def select_price(update: Update, context: CallbackContext) -> int:
    selected_price = update.message.text.replace(' ', '').split('-')
    context.user_data['selected_price'] = selected_price
    city = context.user_data['selected_city']
    category = context.user_data['selected_category']
    price = context.user_data['selected_price']
    queryset = Ad.objects.filter(
        Q(
            realty__in=Realty.objects.filter(
                city__title=city,
                categories__title=category
            )
        ),
        Q(price__gte=int(price[0]), price__lte=int(price[1])) | Q(price=None)
    )
    if len(queryset.all()) > 0:
        for ad in queryset:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Добавить в избранное",
                        callback_data=f'{str(FAVORITE)},{ad.pk}'
                    ),
                    InlineKeyboardButton(
                        "Комментарии",
                        callback_data=f'{str(COMMENT)},{ad.pk}'
                    ),
                ],
            ]
            if ad.price is not None:
                price_in_ad = ad.price
            else:
                price_in_ad = 'Цена не указана'
            await update.message.reply_text(
                f'{ad.pk}\n'
                f'{ad.title.upper()}\n'
                f'{price_in_ad}\n'
                f'{ad.address}\n',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    else:
        await update.message.reply_text(
            'Мы не смогли найти объявления по заданным критериям\n'
            'Вот здания, которые подходят под Ваш запрос:'
        )
        for realty in Realty.objects.filter(
                city__title=city,
                categories__title=category
        ):
            await update.message.reply_text(
                f'{realty.pk}\n'
                f'{realty.title}\n'
                f'{realty.number}\n'
                f'{realty.email}'
            )

    context.user_data.clear()

    return ConversationHandler.END


async def comment(update: Update, context: CallbackContext):
    # id_ad = update.callback_query.data.split(',')[1] - id объявления
    pass


async def favorite(update: Update, context: CallbackContext):
    pass


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
        PRICE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, select_price)
        ],
    },
    fallbacks=[],
)
comment_handler = CallbackQueryHandler(comment, pattern="^" + str(COMMENT))
favorite_handler = CallbackQueryHandler(favorite, pattern="^" + str(FAVORITE))
