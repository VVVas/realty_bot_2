from telegram import Update
from telegram.ext import CallbackContext

from bot.handlers_ import start

START, CITY, CITY_CHOICE, CATEGORY, PRICE = range(5)
FAVORITE, ADD_FAVORITE, DELETE_FAVORITE = range(5, 8)
COMMENT, ADD_COMMENT, COMMENT_INPUT, NEXT_PAGE = range(8, 12)


async def cancel(update: Update, context: CallbackContext) -> int:
    """
    Выход из диалога на любом этапе.

    START_OVER для изменения приветственного сообщения.
    """
    context.user_data['START_OVER'] = True
    return await start(update, context)
