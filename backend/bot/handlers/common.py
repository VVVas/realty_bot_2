from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext

from users.models import Profile

from . import constants
from .constants import START
from .permissions import restricted
from .utils import get_botmessage_by_keyword


@restricted
async def start(update: Update, context: CallbackContext) -> int:
    """Вход в диалог."""
    greeting_message = await get_botmessage_by_keyword('WELCOME')
    if context.user_data.get('START_OVER'):
        greeting_message = await get_botmessage_by_keyword('START_OVER')
    context.user_data.clear()

    if not await Profile.objects.filter(
        external_id=update.effective_user.id
    ).aexists():
        await Profile.objects.acreate(
            external_id=update.effective_user.id,
            username=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name
        )
    keyboard = [
        [constants.BUTTON_SEARCH, constants.BUTTON_ABOUT],
        [constants.BUTTON_FAVORITE, constants.BUTTON_DELETE_USER]
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
    """Вывод информацию о боте."""
    await update.message.reply_text(
        await get_botmessage_by_keyword('BOT_DESCRIPTION')
    )
    return await cancel(update, context)


async def cancel(update: Update, context: CallbackContext) -> int:
    """Возврат в начало с заменой приветствия."""
    context.user_data['START_OVER'] = True
    return await start(update, context)
