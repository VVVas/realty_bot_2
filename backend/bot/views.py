import json

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from . import bot_init


@csrf_exempt
async def webhook(request: HttpRequest) -> HttpResponse:
    """Обрабатываем полученное от бота сообщение."""
    try:
        json_message = json.loads(request.body)
    except json.decoder.JSONDecodeError as err:
        return HttpResponse(str(err))
    await bot_init.tgbot.ptb_app.update_queue.put(
        Update.de_json(
            data=json_message,
            bot=bot_init.tgbot.ptb_app.bot)
    )
    return HttpResponse()
