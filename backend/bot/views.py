import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from .bot_init import APPLICATION


@csrf_exempt
def process(request):
    data = json.loads(request.body.decode())
    update = Update.de_json(data, APPLICATION.bot)
    APPLICATION.process_update(update)

    return JsonResponse({})
