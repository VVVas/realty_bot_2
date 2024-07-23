from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from realties.models import Favorite, Realty
from users.models import Profile

from . import constants
from .constants import ADD_FAVORITE, COMMENT, DELETE_FAVORITE
from .common import cancel
from .utils import edit_message_by_type, text_ad


async def favorite(update: Update, context: CallbackContext):
    """Выводим список избранного."""
    user_id = update.message.from_user.id
    favorite_ads = Favorite.objects.filter(
        user__external_id=user_id
    )
    if not await favorite_ads.aexists():
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


async def add_favorite(update: Update, context: CallbackContext):
    """Добавить объявление в избранное."""
    query = update.callback_query
    await query.answer()
    query_data = query.data.replace(' ', '').split(',')
    user = await Profile.objects.aget(external_id=update.effective_user.id)
    _, created = await Favorite.objects.aget_or_create(
        user=user,
        ad_id=query_data[1]
    )
    if not created:
        await edit_message_by_type(
            update, 'Объявление было добавлено в избранное ранее.'
        )
        return
    await edit_message_by_type(
        update, 'Объявление добавлено в избранное.'
    )


async def delete_favorite(update: Update, context: CallbackContext):
    """Убираем объявление из избранного."""
    query_data = update.callback_query.data.replace(' ', '').split(',')
    if len(query_data) != 3:
        await edit_message_by_type(
            update, 'Некорректные данные для удаления.'
        )
        return
    try:
        await Favorite.objects.filter(
            user__external_id=query_data[2], ad__pk=query_data[1]
        ).adelete()
        await edit_message_by_type(
            update, 'Объявление удалено из избранного.'
        )
    except Favorite.DoesNotExist:
        await edit_message_by_type(
            update, 'Объявление не найдено в избранном.'
        )
    except Exception:
        await edit_message_by_type(
            update, 'Произошла ошибка при удалении записи из избранного.'
        )

add_handler = CallbackQueryHandler(
    add_favorite, pattern="^" + str(ADD_FAVORITE)
)

delete_handler = CallbackQueryHandler(
    delete_favorite, pattern="^" + str(DELETE_FAVORITE)
)
