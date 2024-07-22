from django.core.paginator import Paginator

from . import constants
from .models import BotMessage


def paginate(queryset, page_number=1):
    """Возвращает содержимое страницы. По умолчанию первой."""
    paginator = Paginator(queryset, constants.QUANTITY_PER_PAGE)
    return paginator.get_page(page_number)


async def get_botmessage_by_keyword(keyword):
    """Сообщение бота из БД."""
    return await BotMessage.objects.filter(
        keyword=keyword
    ).values_list('text', flat=True).afirst()


def chunks(lst, chunk_size=3):
    """Создание чанков для кнопок. По 3 в ряд."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def text_ad(ad):
    """Текст выводимый для объявлений."""
    text = f'{ad.title}\n'
    if ad.price:
        text += f'Цена: {ad.price}'
    else:
        text += 'Цена: не указана'
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
    if ad.realty.site:
        text += f'\n{ad.realty.site}'
    if ad.realty.additional_information:
        text += f'\n\n{ad.realty.additional_information}'
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
    if realty.site:
        text += f'\n{realty.site}'
    if realty.additional_information:
        text += f'\n\n{realty.additional_information}'
    if realty.city.timezone:
        text += f'\nЧасовой пояс (по UTC): {realty.city.timezone}'
    return text


def split_query(update):
    return update.callback_query.data.replace(' ', '').split(',')
