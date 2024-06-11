import asyncio
import logging
import os

import django
import uvicorn
from django.conf import settings
from django.core.asgi import get_asgi_application
from telegram import Update

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realty.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from bot import bot_init  # noqa E402

URL = settings.GENERAL_URL  # Set URL for WebHook


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
