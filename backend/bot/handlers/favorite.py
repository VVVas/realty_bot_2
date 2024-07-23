from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.helpers import effective_message_type
from telegram.constants import MessageType

from bot.utils import split_query, text_ad
from realties.models import Favorite, Realty
from users.models import Profile

from bot import constants
from bot.handlers3 import cancel

START, CITY, CITY_CHOICE, CATEGORY, PRICE = range(5)
FAVORITE, ADD_FAVORITE, DELETE_FAVORITE = range(5, 8)
COMMENT, ADD_COMMENT, COMMENT_INPUT, NEXT_PAGE = range(8, 12)


async def add_to_favorite(update: Update, context: CallbackContext):
    """Добавить объявление в избранное."""
    query = update.callback_query
    await query.answer()
    query_data = query.data.split(',')
    user = Profile.objects.get(external_id=update.effective_user.id)
    _, created = Favorite.objects.get_or_create(
        user=user,
        ad_id=query_data[1]
    )
    if not created:
        if effective_message_type(
            update.callback_query.message
        ) == MessageType.TEXT:
            await update.callback_query.edit_message_text(
                "Объявление было добавлено в избранное ранее."
            )
        elif effective_message_type(
            update.callback_query.message
        ) == MessageType.PHOTO:
            await update.callback_query.edit_message_caption(
                "Объявление было добавлено в избранное ранее."
            )
        return
    if effective_message_type(
        update.callback_query.message
    ) == MessageType.TEXT:
        await update.callback_query.edit_message_text(
            "Объявление добавлено в избранное."
        )
    elif effective_message_type(
        update.callback_query.message
    ) == MessageType.PHOTO:
        await update.callback_query.edit_message_caption(
            "Объявление добавлено в избранное."
        )


async def favorite(update: Update, context: CallbackContext):
    """Выводим список избранного."""
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
                    constants.BUTTON_DELETE_FAVORITE,
                    callback_data=f'{str(DELETE_FAVORITE)},'
                                  f'{favorite_ad.ad_id},'
                                  f'{user_id}'
                ),
                InlineKeyboardButton(
                    constants.BUTTON_COMMENTS,
                    callback_data=f'{str(COMMENT)},{favorite_ad.ad_id}'
                ),
            ],
        ]
        img = Realty.objects.get(pk=favorite_ad.ad.realty.pk).img
        if img:
            await update.message.reply_photo(
                photo=img,
                caption=text_ad(favorite_ad.ad),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text(
                text=text_ad(favorite_ad.ad),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    return await cancel(update, context)


async def delete_favorite(update: Update, context: CallbackContext):
    """Убираем объявление из избранного."""
    query_data = split_query(update)
    if len(query_data) != 3:
        if effective_message_type(
            update.callback_query.message
        ) == MessageType.TEXT:
            await update.callback_query.edit_message_text(
                'Некорректные данные для удаления.'
            )
        elif effective_message_type(
            update.callback_query.message
        ) == MessageType.PHOTO:
            await update.callback_query.edit_message_caption(
                'Некорректные данные для удаления.'
            )
        return
    try:
        Favorite.objects.get(
            user__external_id=query_data[2], ad__pk=query_data[1]
        ).delete()
        if effective_message_type(
            update.callback_query.message
        ) == MessageType.TEXT:
            await update.callback_query.edit_message_text(
                'Запись удалена из избранного!'
            )
        elif effective_message_type(
            update.callback_query.message
        ) == MessageType.PHOTO:
            await update.callback_query.edit_message_caption(
                'Запись удалена из избранного!'
            )
    except Favorite.DoesNotExist:
        if effective_message_type(
            update.callback_query.message
        ) == MessageType.TEXT:
            await update.callback_query.edit_message_text(
                'Эта запись не найдена в вашем избранном.'
            )
        elif effective_message_type(
            update.callback_query.message
        ) == MessageType.PHOTO:
            await update.callback_query.edit_message_caption(
                'Эта запись не найдена в вашем избранном.'
            )
    except Exception:
        if effective_message_type(
            update.callback_query.message
        ) == MessageType.TEXT:
            await update.callback_query.edit_message_text(
                'Произошла ошибка при удалении записи из избранного.'
            )
        elif effective_message_type(
            update.callback_query.message
        ) == MessageType.PHOTO:
            await update.callback_query.edit_message_caption(
                'Произошла ошибка при удалении записи из избранного.'
            )

favorite_handler = CallbackQueryHandler(
    add_to_favorite, pattern="^" + str(ADD_FAVORITE)
)

delete_favorite_handler = CallbackQueryHandler(
    delete_favorite, pattern="^" + str(DELETE_FAVORITE)
)
