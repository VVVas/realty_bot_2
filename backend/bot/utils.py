async def aget_botmessage_by_keyword(keyword):
    from bot.models import BotMessage
    return BotMessage.objects.filter(
        keyword=keyword
    ).values_list('text', flat=True).afirst()


def get_botmessage_by_keyword(keyword):
    from bot.models import BotMessage
    return BotMessage.objects.filter(
        keyword=keyword
    ).values_list('text', flat=True).first()
