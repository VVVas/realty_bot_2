import json
import logging

from django.http import JsonResponse
from django.views import View
from telegram import Update

from .bot_init import APPLICATION


logger = logging.getLogger(__name__)


class TelegramBotView(View):

    def post(self, request, *args, **kwargs):
        logger.info("Webhook received")
        try:
            update = Update.de_json(json.loads(request.body), APPLICATION)

            async def process_update():
                logger.info("Processing update")
                await APPLICATION.process_update(update)

            APPLICATION.create_task(process_update())
            return JsonResponse({"status": "ok"})
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"status": "error"}, status=500)
