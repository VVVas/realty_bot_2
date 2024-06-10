import json
import logging

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from telegram import Update

from bot.bot_init import tgbot


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramBotView(View):

    def post(self, request, *args, **kwargs):
        update = Update.de_json(json.loads(request.body), tgbot.ptb_app)

        async def process_update():
            await tgbot.ptb_app.process_update(update)

        tgbot.ptb_app.create_task(process_update())

        return JsonResponse({"status": "ok"})
