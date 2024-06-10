import asyncio
import json
import logging
import os

import django
import uvicorn
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realty.settings')
django.setup()

from tg_bot import tgbot_core  # noqa E402


URL = settings.GENERAL_URL  # Set URL for WebHook
PORT = 8000


@csrf_exempt
async def webhook(request: HttpRequest) -> HttpResponse:
    """Обрабатываем полученное от бота сообщение."""
    await tgbot_core.tgbot.ptb_app.update_queue.put(
        Update.de_json(
            data=json.loads(request.body),
            bot=tgbot_core.tgbot.ptb_app.bot)
    )
    return HttpResponse()


async def main():
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=get_asgi_application(),
            port=PORT,
            use_colors=True,
            host=URL,
            log_level=logging.DEBUG,
        )
    )

    await tgbot_core.tgbot.ptb_app.bot.setWebhook(
        url=f'{URL}/webhook/',
        allowed_updates=Update.ALL_TYPES,
    )

    async with tgbot_core.tgbot.ptb_app:
        await tgbot_core.tgbot.ptb_app.start()
        await webserver.serve()
        await tgbot_core.tgbot.ptb_app.stop()


if __name__ == '__main__':
    asyncio.run(main())
