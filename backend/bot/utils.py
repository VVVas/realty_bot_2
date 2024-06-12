def get_botmessage_by_keyword(keyword):
    from bot.models import BotMessage
    return BotMessage.objects.filter(
        keyword=keyword
    ).values_list('text', flat=True).first()


def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


# async def aget_botmessage_by_keyword(keyword):
#     from bot.models import BotMessage
#     return BotMessage.objects.filter(
#         keyword=keyword
#     ).values_list('text', flat=True).afirst()
