import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from bot.bot_init import BOT, DISPATCHER


@csrf_exempt
def process(request):
    data = json.loads(request.body.decode())
    update = Update.de_json(data, BOT)
    DISPATCHER.process_update(update)

    return JsonResponse({})
