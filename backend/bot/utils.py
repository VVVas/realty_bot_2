def get_botmessage_by_keyword(keyword):
    from bot.models import BotMessage
    return BotMessage.objects.filter(
        keyword=keyword
    ).values_list('text', flat=True).first()


def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def text_ad(ad):
    if ad.price is not None:
        price_in_ad = ad.price
    else:
        price_in_ad = 'Цена не указана'
    return (f'{ad.pk}\n '
            f'{ad.title.upper()}\n '
            f'Цена: {price_in_ad}\n '
            f'Адрес: {ad.address}\n '
            f'Дополнительная информация: {ad.additional_information}\n'
            f'\n'
            f'Находится в здании: {ad.realty.title}\n'
            f'По адресу: {ad.realty.address}'
            f'Номера для связи: '
            f'{ad.realty.phone_number} '
            f'{ad.realty.mobile_number} '
            f'{ad.realty.number}\n '
            f'Электронная почта для связи: {ad.realty.email}\n '
            f'айт организации: {ad.realty.site}\n'
            f'Дополнительная информация:  {ad.realty.additional_information}')


def text_realty(realty):
    return (f'{realty.title}\n'
            f'По адресу: {realty.address}'
            f'Номера для связи: '
            f'{realty.phone_number} '
            f'{realty.mobile_number} '
            f'{realty.number}\n '
            f'Электронная почта для связи: {realty.email}\n '
            f'айт организации: {realty.site}\n'
            f'Дополнительная информация:  {realty.additional_information}')


# async def aget_botmessage_by_keyword(keyword):
#     from bot.models import BotMessage
#     return BotMessage.objects.filter(
#         keyword=keyword
#     ).values_list('text', flat=True).afirst()
