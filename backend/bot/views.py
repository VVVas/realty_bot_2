import json

from django.conf import settings
from django.http import JsonResponse
from django.views import View
from telegram import Update

from .bot_init import tgbot


class TelegramBotView(View):

    def post(self, request, *args, **kwargs):
        update = Update.de_json(json.loads(request.body), tgbot.ptb_app)

        async def process_update():
            await tgbot.ptb_app.process_update(update)

        tgbot.ptb_app.create_task(process_update())

        return JsonResponse({"status": "ok"})
