from django.core.paginator import Paginator

from .models import BotMessage

QUANTITY_PER_PAGE = 10


def paginate(queryset, page_number=1):
    """Возвращает содержимое страницы. По умолчанию первой."""
    paginator = Paginator(queryset, QUANTITY_PER_PAGE)
    return paginator.get_page(page_number)


def get_botmessage_by_keyword(keyword):
    """Сообщение бота из БД."""
    return BotMessage.objects.filter(
        keyword=keyword
    ).values_list('text', flat=True).first()


def chunks(lst, chunk_size=3):
    """Создание чанков для кнопок. По 3 в ряд."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def text_ad(ad):
    """Текст выводимый для объявлений."""
    if ad.price is not None:
        price_in_ad = ad.price
    else:
        price_in_ad = 'не указана'
    return (f'{ad.title.upper()}\n\n'
            f'Цена: {price_in_ad}\n'
            f'{ad.additional_information}\n\n'
            f'Расположение\n'
            f'{ad.realty.title}\n'
            f'{ad.realty.address}\n'
            f'{ad.address}\n'
            f'{ad.realty.phone_number} '
            f'{ad.realty.mobile_number} '
            f'{ad.realty.number}\n'
            f'{ad.realty.email}\n'
            f'{ad.realty.site}\n\n'
            f'{ad.realty.additional_information}')


def text_realty(realty):
    """Текст выводимый для недвижимости."""
    text = f'{realty.title}\n'
    if realty.address:
        text += f'\n{realty.address}'
    if any(
        realty.phone_number,
        realty.mobile_number,
        realty.number
    ):
        text += '\n'
        if realty.phone_number:
            text += f'{realty.phone_number} '
        if realty.mobile_number:
            text += f'{realty.mobile_number} '
        if realty.number:
            text += f'{realty.number}'
    if realty.email:
        text += f'\n{realty.email}'
    if realty.site:
        text += f'\n{realty.site}'
    if realty.additional_information:
        text += f'\n\n{realty.additional_information}'
    return text


def split_query(update):
    return update.callback_query.data.replace(' ', '').split(',')
