import re

from django.db.models import Q

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          MessageHandler, filters)

from realties.models import Ad, Category, City, Realty
from users.models import Profile

import constants
from .common import cancel, help_command, start
from .constants import (ADD_COMMENT, ADD_FAVORITE, CATEGORY, CITY, CITY_CHOICE,
                        COMMENT, NEXT_PAGE, PRICE, START)
from .favorite import favorite
from .user import delete_user
from .utils import (chunks, get_botmessage_by_keyword, paginate, text_ad,
                    text_realty)


async def start_work(update: Update, context: CallbackContext) -> int:
    """Начало диалоговой цепочки о поиске объявлений."""
    await update.message.reply_text(
        await get_botmessage_by_keyword('START_WORK')
    )

    return CITY_CHOICE


async def city_choice(update: Update, context: CallbackContext) -> int:
    """Выбор города."""
    city_name = update.message.text.lower()
    list_names = [city.title for city in City.objects.all()]
    list_cities = []
    for city in list_names:
        if city.lower().startswith(city_name):
            list_cities.append(city)
    if len(list_cities) < 1:
        await update.message.reply_text(
            await get_botmessage_by_keyword('CITY_CHOICE_NOT')
        )
        return CITY_CHOICE
    list_chunks = list(chunks(list_cities))
    keyboard = [chunk for chunk in list_chunks]
    await update.message.reply_text(
        await get_botmessage_by_keyword('CITY_CHOICE'),
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return CITY


async def select_city(update: Update, context: CallbackContext) -> int:
    """Выбор категории из БД. Можно пропустить. Запоминаем город."""
    list_names = [category.title for category in Category.objects.all()]
    list_chunks = list(chunks(list_names))
    keyboard = [chunk for chunk in list_chunks]
    keyboard.append([constants.BUTTON_SKIP])
    selected_city = update.message.text
    context.user_data['selected_city'] = selected_city
    await update.message.reply_text(
        await get_botmessage_by_keyword('CATEGORY_CHOICE'),
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return CATEGORY


async def select_category(update: Update, context: CallbackContext) -> int:
    """Фильтрация по цене. Можно пропустить. Запоминаем категорию."""
    selected_category = update.message.text
    if selected_category.lower() == constants.BUTTON_SKIP.lower():
        context.user_data['selected_category'] = None
    else:
        context.user_data['selected_category'] = selected_category
    await update.message.reply_text(
        await get_botmessage_by_keyword('PRICE_INPUT'),
        reply_markup=ReplyKeyboardMarkup(
            [[constants.BUTTON_SKIP]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )

    return PRICE


async def select_price(update: Update, context: CallbackContext) -> int:
    """Вывод списка объявлений и объектов. Запоминаем цену."""
    selected_price = update.message.text.replace(' ', '').split('-')
    if (selected_price[0].lower() == constants.BUTTON_SKIP.lower()
            or int(selected_price[1]) == 0):
        context.user_data['selected_price'] = None
    else:
        context.user_data['selected_price'] = selected_price
    city = context.user_data.get('selected_city')
    category = context.user_data.get('selected_category')
    price = context.user_data.get('selected_price')
    filters = Q(is_published=True)
    if city:
        filters &= Q(realty__city__title=city)
    if category:
        filters &= Q(realty__categories__title=category)
    if price:
        filters &= Q(
            price__gte=int(price[0]), price__lte=int(price[1])
        ) | Q(price=None)
    ad_queryset = Ad.objects.filter(filters)
    if ad_queryset.exists():

        user_profile = Profile.objects.get(
            external_id=update.effective_user.id
        )

        items = paginate(ad_queryset)

        for item in items:
            keyboard = [
                [
                    InlineKeyboardButton(
                        constants.BUTTON_ADD_FAVORITE,
                        callback_data=f'{str(ADD_FAVORITE)},{item.pk}'
                    ),
                    InlineKeyboardButton(
                        constants.BUTTON_COMMENTS,
                        callback_data=f'{str(COMMENT)},{item.pk}'
                    ),
                ],
            ]

            if user_profile.is_active:
                keyboard[0].append(
                    InlineKeyboardButton(
                        constants.BUTTON_ADD_COMMENT,
                        callback_data=f'{str(ADD_COMMENT)},{item.pk}'
                    )
                )

            img = Realty.objects.get(pk=item.realty_id).img

            if img:
                await update.message.reply_photo(
                    photo=img,
                    caption=text_ad(item),
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await update.message.reply_text(
                    text=text_ad(item),
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )

        if items.has_next():
            context.user_data['page'] = items.next_page_number()
            await update.message.reply_text(
                f'Вы посмотрели первые {constants.QUANTITY_PER_PAGE} '
                'элементов',
                reply_markup=ReplyKeyboardMarkup(
                    [[constants.BUTTON_NEXT]],
                    one_time_keyboard=True,
                    resize_keyboard=True
                )
            )
            return NEXT_PAGE

    else:
        realty_filters = Q(city__title=city)
        if category:
            realty_filters &= Q(categories__title=category)
        realty_queryset = Realty.objects.filter(realty_filters)

        if realty_queryset.exists():
            await update.message.reply_text(
                await get_botmessage_by_keyword('ADS_NOT_FOUND')
            )

            items = paginate(realty_queryset)

            for item in items:

                if item.img:
                    await update.message.reply_photo(
                        photo=item.img,
                        caption=text_realty(item)
                    )
                else:
                    await update.message.reply_text(
                        text_realty(item)
                    )

            if items.has_next():
                context.user_data['page'] = items.next_page_number()
                await update.message.reply_text(
                    f'Вы посмотрели первые {constants.QUANTITY_PER_PAGE} '
                    'элементов',
                    reply_markup=ReplyKeyboardMarkup(
                        [[constants.BUTTON_NEXT]],
                        one_time_keyboard=True,
                        resize_keyboard=True
                    )
                )
                return NEXT_PAGE
        else:
            await update.message.reply_text(
                await get_botmessage_by_keyword('REALTIES_NOT_FOUND')
            )

    context.user_data.clear()

    return await cancel(update, context)


async def next_page(update: Update, context: CallbackContext) -> int:
    """Следующая страинца для списка объявлений и объектов."""
    city = context.user_data.get('selected_city')
    category = context.user_data.get('selected_category')
    price = context.user_data.get('selected_price')
    page = context.user_data.get('page')
    filters = Q(is_published=True)
    if city:
        filters &= Q(realty__city__title=city)
    if category:
        filters &= Q(realty__categories__title=category)
    if price:
        filters &= Q(
            price__gte=int(price[0]), price__lte=int(price[1])
        ) | Q(price=None)
    ad_queryset = Ad.objects.filter(filters)
    if ad_queryset.exists():

        user_profile = Profile.objects.get(
            external_id=update.effective_user.id
        )

        items = paginate(ad_queryset, page)

        for item in items:

            keyboard = [
                [
                    InlineKeyboardButton(
                        constants.BUTTON_ADD_FAVORITE,
                        callback_data=f'{str(ADD_FAVORITE)},{item.pk}'
                    ),
                    InlineKeyboardButton(
                        constants.BUTTON_COMMENTS,
                        callback_data=f'{str(COMMENT)},{item.pk}'
                    ),
                ],
            ]

            if user_profile.is_active:
                keyboard[0].append(
                    InlineKeyboardButton(
                        constants.BUTTON_ADD_COMMENT,
                        callback_data=f'{str(ADD_COMMENT)},{item.pk}'
                    )
                )

            img = Realty.objects.get(pk=item.realty_id).img
            if img:
                await update.message.reply_photo(
                    photo=img,
                    caption=text_ad(item),
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await update.message.reply_text(
                    text=text_ad(item),
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )

        if items.has_next():
            context.user_data['page'] = items.next_page_number()
            await update.message.reply_text(
                f'Вы посмотрели {items.end_index()} элементов '
                f'из {ad_queryset.count()}',
                reply_markup=ReplyKeyboardMarkup(
                    [[constants.BUTTON_NEXT]],
                    one_time_keyboard=True,
                    resize_keyboard=True
                )
            )
            return NEXT_PAGE

    else:
        realty_filters = Q(city__title=city)
        if category:
            realty_filters &= Q(categories__title=category)
        realty_queryset = Realty.objects.filter(realty_filters)

        if realty_queryset.exists():
            await update.message.reply_text(
                await get_botmessage_by_keyword('ADS_NOT_FOUND')
            )

            items = paginate(realty_queryset, page)

            for item in items:
                if item.img:
                    await update.message.reply_photo(
                        photo=item.img,
                        caption=text_realty(item)
                    )
                else:
                    await update.message.reply_text(
                        text_realty(item)
                    )

            if items.has_next():
                context.user_data['page'] = items.next_page_number()
                await update.message.reply_text(
                    f'Вы посмотрели {items.end_index()} элементов '
                    f'из {realty_queryset.count()}',
                    reply_markup=ReplyKeyboardMarkup(
                        [[constants.BUTTON_NEXT]],
                        one_time_keyboard=True,
                        resize_keyboard=True
                    )
                )
                return NEXT_PAGE

    context.user_data.clear()

    return await cancel(update, context)


search_conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start)
    ],
    states={
        START: [
            MessageHandler(
                filters.Regex(
                    re.compile(r'^(' + constants.BUTTON_SEARCH + ')$',
                               re.IGNORECASE)
                ), start_work
            ),
            MessageHandler(
                filters.Regex(
                    re.compile(r'^(' + constants.BUTTON_ABOUT + ')$',
                               re.IGNORECASE)
                ), help_command
            ),
            MessageHandler(
                filters.Regex(
                    re.compile(r'^(' + constants.BUTTON_FAVORITE + ')$',
                               re.IGNORECASE)
                ), favorite
            ),
            MessageHandler(
                filters.Regex(
                    re.compile(r'^(' + constants.BUTTON_DELETE_USER + ')$',
                               re.IGNORECASE)
                ), delete_user
            ),
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
        NEXT_PAGE: [
            MessageHandler(
                filters.Regex(
                    re.compile(r'^(' + constants.BUTTON_NEXT + ')$',
                               re.IGNORECASE)
                ), next_page
            ),
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True,
)
