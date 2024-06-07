import logging

from django.conf import settings
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler


from realties.models import Ad

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
TITLE, ADDRESS, ADDITIONAL_INFO = range(3)


logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start command")
    await update.message.reply_text(
        'Hello! Use /ads to see the list of ads, '
        '/filter <category> to filter ads by category, '
        'and /new to create a new ad.')


async def ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /ads command")
    ads_list = Ad.objects.filter(is_published=True)
    if ads_list:
        for ad in ads_list:
            realty = ad.realty
            caption = (
                f"*{ad.title}*\n"
                f"Объект: {ad.realty}\n"
                f"Точный адрес объявления: {ad.address}"
                f"Дополнительная информация: {ad.additional_information}\n"
                f"Дата добавления: {ad.date}")
            if realty.img:
                await context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=realty.img.url,
                    caption=caption,
                    parse_mode='Markdown'
                )
            else:
                await context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=caption,
                    parse_mode='Markdown'
                )
    else:
        response = "No ads available."
        await context.bot.send_message(
            chat_id=update.message.chat_id, text=response)


async def filter_ad_category(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    category = context.args[0]
    ads_list = Ad.objects.filter(
        is_published=True, realty__category__title=category
    )
    if ads_list:
        for ad in ads_list:
            realty = ad.realty
            caption = (
                f"*{ad.title}*\n"
                f"Объект: {ad.realty}\n"
                f"Точный адрес объявления: {ad.address}"
                f"Дополнительная информация: {ad.additional_information}\n"
                f"Дата добавления: {ad.date}")
            if realty.img:
                await context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=realty.img.url,
                    caption=caption,
                    parse_mode='Markdown'
                )
            else:
                await context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=caption,
                    parse_mode='Markdown'
                )
    else:
        response = "No ads available."
        await context.bot.send_message(
            chat_id=update.message.chat_id, text=response)


async def new_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Please send the title of the ad.'
    )
    return TITLE


async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_ad_title'] = update.message.text
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Now please send the address of the ad.'
    )
    return ADDRESS


async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_ad_adsress'] = update.message.text
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Now please send the address of the ad.'
    )
    return ADDITIONAL_INFO


async def get_additional_info(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    title = context.user_data['new_ad_title']
    address = context.user_data['new_ad_adsress']
    additional_information = update.message.text
    Ad.objects.create(
        title=title, address=address,
        additional_information=additional_information
    )
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Thank you! Ad "{title}" created successfully!'
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Operation cancelled.')
    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('new_ad', new_ad)],
    states={
        TITLE: [CommandHandler('title', get_title)],
        ADDRESS: [CommandHandler('address', get_address)],
        ADDITIONAL_INFO: [CommandHandler(
            'additional_info', get_additional_info
        )]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
