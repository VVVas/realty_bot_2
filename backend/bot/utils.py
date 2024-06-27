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
    return (f'{realty.title}\n\n'
            f'{realty.address}\n'
            f'{realty.phone_number} '
            f'{realty.mobile_number} '
            f'{realty.number}\n '
            f'{realty.email}\n'
            f'{realty.site}\n\n'
            f'{realty.additional_information}')


def split_query(update):
    return update.callback_query.data.replace(' ', '').split(',')
