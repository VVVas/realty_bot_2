from django.core.paginator import Page, Paginator
from django.db.models import Q
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext
from telegram.helpers import effective_message_type
from telegram.constants import MessageType

from ..models import BotMessage
from . import constants


def paginate(queryset, page_number=1):
    """Возвращает содержимое страницы. По умолчанию первой."""
    paginator = Paginator(queryset, constants.QUANTITY_PER_PAGE)
    return paginator.get_page(page_number)


async def get_message_and_keyboard_for_next_page(items: Page, update: Update):
    """Отправляет сообщение переходе на следующую странцу."""
    await update.message.reply_text(
        f'Страница {items.number} из {items.paginator.num_pages} страниц.',
        reply_markup=ReplyKeyboardMarkup(
            [[constants.BUTTON_NEXT]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )


async def get_botmessage_by_keyword(keyword):
    """Возвращает сообщение для бота из БД."""
    return await BotMessage.objects.filter(
        keyword=keyword
    ).values_list('text', flat=True).afirst()


async def edit_message_by_type(update: Update, text: str):
    """Редактирует текст в сообщении типа текст и фото."""
    if effective_message_type(
        update.callback_query.message
    ) == MessageType.TEXT:
        await update.callback_query.edit_message_text(text)
    elif effective_message_type(
        update.callback_query.message
    ) == MessageType.PHOTO:
        await update.callback_query.edit_message_caption(text)


def get_realty_filters(context: CallbackContext):
    """Собирает и возвращает фильтр недвижимости."""
    city = context.user_data.get('selected_city')
    category = context.user_data.get('selected_category')
    realty_filters = Q(city__title=city)
    if category:
        realty_filters &= Q(categories__title=category)
    return realty_filters


def get_ad_filters(context: CallbackContext):
    """Собирает и возвращает фильр объявлений."""
    city = context.user_data.get('selected_city')
    category = context.user_data.get('selected_category')
    price = context.user_data.get('selected_price')
    ad_filters = Q(realty__city__title=city, is_published=True)
    if category:
        ad_filters &= Q(realty__categories__title=category)
    if price:
        ad_filters &= Q(
            price__gte=int(price[0]), price__lte=int(price[1])
        ) | Q(price=None)
    return ad_filters


def chunks(lst, chunk_size=3):
    """Создание чанков для кнопок. По умолчанию 3 в ряд."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def text_ad(ad):
    """Текст выводимый для объявлений."""
    text = f'{ad.title}\n'
    if ad.price:
        text += f'Цена за кв. м.: {ad.price} руб.'
    else:
        text += 'Цена не указана'
    if ad.additional_information:
        text += f'\n{ad.additional_information}'
    text += f'\n\nРасположение\n{ad.realty.title}'
    if ad.realty.address:
        text += f'\n{ad.realty.address}'
    if ad.address:
        text += f'\n{ad.address}'
    if any(
        [ad.realty.phone_number, ad.realty.mobile_number, ad.realty.number]
    ):
        text += '\n'
        if ad.realty.phone_number:
            text += f'{ad.realty.phone_number} '
        if ad.realty.mobile_number:
            text += f'{ad.realty.mobile_number} '
        if ad.realty.number:
            text += ad.realty.number
        text.rstrip()
    if ad.realty.email:
        text += f'\n{ad.realty.email}'
    if ad.realty.contact_name:
        text += f'\n{ad.realty.contact_name}'
    if ad.realty.site:
        text += f'\n{ad.realty.site}'
    if ad.realty.additional_information:
        text += f'\n\n{ad.realty.additional_information}'
    if ad.realty.city.timezone:
        text += f'\nЧасовой пояс (по UTC): {ad.realty.city.timezone}'
    return text


def text_realty(realty):
    """Текст выводимый для недвижимости."""
    text = f'{realty.title}\n'
    if realty.address:
        text += f'\n{realty.address}'
    if any([realty.phone_number, realty.mobile_number, realty.number]):
        text += '\n'
        if realty.phone_number:
            text += f'{realty.phone_number} '
        if realty.mobile_number:
            text += f'{realty.mobile_number} '
        if realty.number:
            text += realty.number
        text.rstrip()
    if realty.email:
        text += f'\n{realty.email}'
    if realty.contact_name:
        text += f'\n{realty.contact_name}'
    if realty.site:
        text += f'\n{realty.site}'
    if realty.additional_information:
        text += f'\n\n{realty.additional_information}'
    if realty.city.timezone:
        text += f'\nЧасовой пояс (по UTC): {realty.city.timezone}'
    return text
