import asyncio
# import json
import logging
import os

import django
import uvicorn
from django.conf import settings
from django.core.asgi import get_asgi_application
# from django.http import HttpRequest, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
from telegram import Update

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realty.settings')
django.setup()

from bot import bot_init  # noqa E402


URL = settings.GENERAL_URL  # Set URL for WebHook


# @csrf_exempt
# async def webhook(request: HttpRequest) -> HttpResponse:
#     """Обрабатываем полученное от бота сообщение."""
#     await tgbot_core.tgbot.ptb_app.update_queue.put(
#         Update.de_json(
#             data=json.loads(request.body),
#             bot=tgbot_core.tgbot.ptb_app.bot)
#     )
#     return HttpResponse()


async def main():
    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=get_asgi_application(),
            port=8000,
            use_colors=True,
            host='0.0.0.0',
            log_level=logging.DEBUG,
        )
    )

    await bot_init.tgbot.ptb_app.bot.setWebhook(
        url=f'{URL}/webhook/',
        allowed_updates=Update.ALL_TYPES,
    )

    async with bot_init.tgbot.ptb_app:
        await bot_init.tgbot.ptb_app.start()
        await webserver.serve()
        await bot_init.tgbot.ptb_app.stop()


if __name__ == '__main__':
    asyncio.run(main())
