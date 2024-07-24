from telegram import Update
from telegram.ext import CallbackContext

from users.models import Profile

from .common import cancel
from .utils import get_botmessage_by_keyword


async def delete_user(update: Update, context: CallbackContext):
    """Удаление пользователя."""
    await Profile.objects.filter(
        external_id=update.message.from_user.id
    ).adelete()
    await update.message.reply_text(
        await get_botmessage_by_keyword('DELETE_PROFILE')
    )
    return await cancel(update, context)
