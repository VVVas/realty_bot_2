from telegram import Update
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          ConversationHandler, MessageHandler,
                          filters)

from realties.models import Comment
from users.models import Profile

START, CITY, CITY_CHOICE, CATEGORY, PRICE = range(5)
FAVORITE, ADD_FAVORITE, DELETE_FAVORITE = range(5, 8)
COMMENT, ADD_COMMENT, COMMENT_INPUT, NEXT_PAGE = range(8, 12)


async def comment(update: Update, context: CallbackContext):
    """Вывод комментариев к объявлению."""
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
    """Добавление комментария к обьявлению."""
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

add_comment_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        add_comment,
        pattern="^" + str(ADD_COMMENT)
    )],
    states={
        COMMENT_INPUT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, comment_input)
        ]
    },
    fallbacks=[],
)

comment_handler = CallbackQueryHandler(
    comment, pattern="^" + str(COMMENT)
)
