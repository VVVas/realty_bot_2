def get_botmessage_by_keyword(keyword):
    """Сообщение бота из БД."""
    from bot.models import BotMessage
    return BotMessage.objects.filter(
        keyword=keyword
    ).values_list('text', flat=True).first()


def chunks(lst, chunk_size):
    """СОздание чанков для кнопок. По 3 в ряд."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def text_ad(ad):
    """Текст выводимый для объявлений."""
    if ad.price is not None:
        price_in_ad = ad.price
    else:
        price_in_ad = 'Цена не указана'
    return (f'{ad.pk}\n'
            f'{ad.title.upper()}\n'
            f'Цена: {price_in_ad}\n'
            f'Адрес: {ad.address}\n'
            f'Дополнительная информация: {ad.additional_information}\n'
            f'\n'
            f'Находится в здании: {ad.realty.title}\n'
            f'По адресу: {ad.realty.address}'
            f'Номера для связи:'
            f'{ad.realty.phone_number} '
            f'{ad.realty.mobile_number} '
            f'{ad.realty.number}\n'
            f'Электронная почта для связи: {ad.realty.email}\n'
            f'Cайт организации: {ad.realty.site}\n'
            f'Дополнительная информация:  {ad.realty.additional_information}')


def text_realty(realty):
    """Текст выводимый для недвижимости."""
    return (f'Некоммерческая площадь: '
            f'{realty.title}\n'
            f'По адресу: {realty.address}\n'
            f'Номера для связи:'
            f'{realty.phone_number} '
            f'{realty.mobile_number} '
            f'{realty.number}\n '
            f'Электронная почта для связи: {realty.email}\n'
            f'Cайт организации: {realty.site}\n'
            f'Дополнительная информация:  {realty.additional_information}')


def split_query(update):
    return update.callback_query.data.replace(' ', '').split(',')
