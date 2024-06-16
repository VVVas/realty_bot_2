from django.db.models import Q
from telegram import (ReplyKeyboardMarkup, Update, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          MessageHandler, filters, CallbackQueryHandler)

from realties.models import Category, City, Comment, Ad, Realty, Favorite
from users.models import Profile
from .utils import (get_botmessage_by_keyword, chunks, text_ad, text_realty,
                    split_query)
from .permissions import restricted


START, CITY, CITY_CHOICE, CATEGORY, PRICE = range(5)
FAVORITE, ADD_FAVORITE, DELETE_FAVORITE = range(5, 8)
COMMENT, ADD_COMMENT, COMMENT_INPUT = range(8, 11)


@restricted
async def start(update: Update, context: CallbackContext) -> int:
    """Вход в диалог."""
    greeting_message = get_botmessage_by_keyword('WELCOME')
    if context.user_data.get('START_OVER'):
        greeting_message = 'Выберите нужное действие'
    context.user_data.clear()
    if not Profile.objects.filter(
        external_id=update.effective_user.id
        # external_id=update.message.from_user.id
    ).exists():
        Profile.objects.create(
            external_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name
        )
    keyboard = [
        ['Начало работы', 'О боте'],
        ['Избранное', 'Удалить учетную запись']
    ]

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
    """Команда предоставляющая информацию о боте."""
    await update.message.reply_text(
        get_botmessage_by_keyword('BOT_DESCRIPTION')
    )
    return await cancel(update, context)


async def start_work(update: Update, context: CallbackContext) -> int:
    """Начало диалоговой цепочки о поиске объявлений."""
    await update.message.reply_text(
        "Давайте начнем поиск объявлений. "
        "Пожалуйста, введите название города"
    )

    return CITY_CHOICE


async def city_choice(update: Update, context: CallbackContext) -> int:
    """Выбор города. Название переводим в нижний кейс."""
    # list_button = [[]]
    list_cities = []
    city_name = update.message.text.lower()
    list_names = [city.title for city in City.objects.all()]
    for city in list_names:
        if city.lower().startswith(city_name):
            list_cities.append(city)
    chunk_size = 3
    list_chunks = list(chunks(list_cities, chunk_size))
    keyboard = [chunk for chunk in list_chunks]
    await update.message.reply_text(
        'Вот какие города я нашёл. Выберите нужный из списка:',
        reply_markup=ReplyKeyboardMarkup(
            # list_button,
            keyboard,
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return CITY


async def select_city(update: Update, context: CallbackContext) -> int:
    """
    Предоставляем выбор из загруженных в БД категорий.

    Возможно пропустить.
    """
    list_names = [category.title for category in Category.objects.all()]
    chunk_size = 3
    list_chunks = list(chunks(list_names, chunk_size))
    keyboard = [chunk for chunk in list_chunks]
    keyboard.append(['Пропустить'])
    selected_city = update.message.text
    context.user_data['selected_city'] = selected_city
    await update.message.reply_text(
        'Отлично! Теперь необходимо '
        'выбрать категорию или пропустить этот шаг.',
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            one_time_keyboard=True
        )
    )
    return CATEGORY


async def select_category(update: Update, context: CallbackContext) -> int:
    """Фильтрация по цене. Выбранную категорию запоминаем для выборки."""
    selected_category = update.message.text
    if selected_category.lower() == "пропустить":
        context.user_data['selected_category'] = None
    else:
        context.user_data['selected_category'] = selected_category
    await update.message.reply_text(
        'Остался последний шаг! Необходимо выбрать ценовой диапозон.\n'
        'Введите его, разделяя цифры тире (-).\n'
        'Например: 10000-20000',
        reply_markup=ReplyKeyboardMarkup(
            [['Пропустить']],
            one_time_keyboard=True
        )
    )

    return PRICE


async def select_price(update: Update, context: CallbackContext) -> int:
    """Выводим список объявлений и завершаем цепочку диалога."""
    selected_price = update.message.text.replace(' ', '').split('-')
    if (selected_price[0].lower() == "пропустить"
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
    queryset = Ad.objects.filter(filters)
    if queryset.exists():
        for ad in queryset:
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Добавить в избранное",
                        callback_data=f'{str(ADD_FAVORITE)},{ad.pk}'
                    ),
                    InlineKeyboardButton(
                        "Комментарии",
                        callback_data=f'{str(COMMENT)},{ad.pk}'
                    ),
                ],
            ]
            user_profile = Profile.objects.get(
                external_id=update.effective_user.id
            )
            if user_profile.is_active:
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "Добавить в избранное",
                            callback_data=f'{str(ADD_FAVORITE)},{ad.pk}'
                        ),
                        InlineKeyboardButton(
                            "Комментарии",
                            callback_data=f'{str(COMMENT)},{ad.pk}'
                        ),
                        InlineKeyboardButton(
                            "Добавить комментарий",
                            callback_data=f'{str(ADD_COMMENT)},{ad.pk}'
                        )
                    ],
                ]
            await update.message.reply_text(
                text=text_ad(ad),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    else:
        realty_filters = Q(city__title=city)
        if category:
            realty_filters &= Q(categories__title=category)
        realty_queryset = Realty.objects.filter(realty_filters)
        if realty_queryset.exists():
            await update.message.reply_text(
                'Мы не смогли найти объявления по заданным критериям\n'
                'Вот здания, которые подходят под Ваш запрос:'
            )
            for realty in realty_queryset:
                await update.message.reply_text(
                    text_realty(realty)
                )
        else:
            await update.message.reply_text(
                'Мы не смогли найти объявления по заданным критериям\n'
                'И не найдено ни одного здания по заданным критериям.'
            )

    context.user_data.clear()

    return await cancel(update, context)


async def comment(update: Update, context: CallbackContext):
    """Вывести комментарии к объявлению."""
    query = update.callback_query
    await query.answer()
    query_data = query.data.split(',')
    comments = Comment.objects.filter(ad=query_data[1], is_published=True)
    if comments.exists():
        for comment in comments:
            await update._bot.send_message(
                text=(
                    f'_{comment.user.first_name}_\n'
                    f'{comment.text}'
                ),
                chat_id=query.message.chat.id,
                parse_mode='Markdown'
            )
    else:
        await update._bot.send_message(
            text='К этому объявлению нет комментариев.',
            chat_id=query.message.chat.id,
            parse_mode='Markdown'
        )


async def add_comment(update: Update, context: CallbackContext):
    """Добавить комментарий к обьявлению."""
    query = update.callback_query
    ad_id = query.data.split(',')[1]
    context.user_data['ad_id'] = ad_id

    await query.answer()
    await update._bot.send_message(
        text="Пожалуйста, введите ваш комментарий:",
        chat_id=query.message.chat.id,
        parse_mode='Markdown'
    )

    return COMMENT_INPUT


async def comment_input(update: Update, context: CallbackContext):
    """Создание комментария. Будет показан после модерации."""
    user_comment = update.message.text
    ad_id = context.user_data.get('ad_id')
    user_id = Profile.objects.get(external_id=update.message.from_user.id).id
    comment = Comment.objects.create(
        ad_id=ad_id,
        user_id=user_id,
        text=user_comment
    )
    comment.save()
    await update.message.reply_text(
        "Ваш комментарий был добавлен и "
        "будет опубликован после проверки администратором."
    )

    return ConversationHandler.END


async def add_to_favorite(update: Update, context: CallbackContext):
    """Добавить объявление в избранное."""
    query = update.callback_query
    await query.answer()
    query_data = query.data.split(',')
    user = Profile.objects.get(external_id=update.effective_user.id)
    fav, res = Favorite.objects.get_or_create(
        user=user,
        ad_id=query_data[1]
    )
    if res:
        await query.edit_message_text(
            "Объявление добавлено в избранное."
        )
    else:
        await query.edit_message_text(
            "Данное объявление уже добавлено в избранное."
        )


async def favorite(update: Update, context: CallbackContext):
    """Показываем список избранного."""
    user_id = update.message.from_user.id
    favorite_ads = Favorite.objects.filter(
        user__external_id=user_id
    )
    if not favorite_ads.exists():
        await update.message.reply_text('У вас нет избранных объявлений.')
    for favorite_ad in favorite_ads:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Удалить из избранного",
                    callback_data=f'{str(DELETE_FAVORITE)},'
                                  f'{favorite_ad.pk},'
                                  f'{user_id}'
                ),
                InlineKeyboardButton(
                    "Комментарии",
                    callback_data=f'{str(COMMENT)},{favorite_ad.pk}'
                ),
            ],
        ]
        await update.message.reply_text(
            text_ad(favorite_ad.ad),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    return await cancel(update, context)


async def delete_favorite(update: Update, context: CallbackContext):
    """Убираем объявление из избранного."""
    query_data = split_query(update)
    if len(query_data) != 3:
        await update.callback_query.edit_message_text(
            'Некорректные данные для удаления.'
        )
        return
    try:
        Favorite.objects.get(
            user__external_id=query_data[2], ad__pk=query_data[1]
        ).delete()
        await update.callback_query.edit_message_text(
            'Запись удалена из избранного!'
        )
    except Favorite.DoesNotExist:
        await update.callback_query.edit_message_text(
            'Эта запись не найдена в вашем избранном.'
        )
    except Exception:
        await update.callback_query.edit_message_text(
            'Произошла ошибка при удалении записи из избранного.'
        )


async def delete_user(update: Update, context: CallbackContext):
    """Удаление пользователя."""
    Profile.objects.get(external_id=update.message.from_user.id).delete()
    await update.message.reply_text(
        get_botmessage_by_keyword('DELETE_PROFILE')
    )
    return await cancel(update, context)


async def cancel(update: Update, context: CallbackContext) -> int:
    """
    Выход из диалога на любом этапе.

    START_OVER для изменения приветственного сообщения.
    """
    context.user_data['START_OVER'] = True
    return await start(update, context)


search_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START: [
            MessageHandler(filters.Regex('^(О боте)$'), help_command),
            MessageHandler(filters.Regex('^(Начало работы)$'), start_work),
            MessageHandler(filters.Regex('^(Избранное)$'), favorite),
            MessageHandler(filters.Regex('^(Удалить)'), delete_user),
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
        COMMENT_INPUT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, comment_input)
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

comment_handler = CallbackQueryHandler(comment, pattern="^" + str(COMMENT))
favorite_handler = CallbackQueryHandler(
    add_to_favorite, pattern="^" + str(ADD_FAVORITE)
)
delete_favorite_handler = CallbackQueryHandler(
    delete_favorite,
    pattern="^" + str(DELETE_FAVORITE)
)
add_comment_handler = CallbackQueryHandler(
    add_comment, pattern="^" + str(ADD_COMMENT)
)
comment_input_handler = MessageHandler(
    filters.TEXT & ~filters.COMMAND, comment_input
)
