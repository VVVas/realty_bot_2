# from django.shortcuts import render
import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler


def index(request):
    return HttpResponse("Hello, world. This is the bot app.")


@csrf_exempt
def talkin_to_me_bruh(request):
    # please insert magic here
    try:
        json_message = json.loads(request.body)
    except json.decoder.JSONDecodeError as err:
        return HttpResponse(str(err))

    return HttpResponse('OK')


async def start(update: Update) -> None:
    """Display a message with instructions on how to use this bot."""
    text = 'VVVas not best!'
    await update.message.reply_html(text=text)


ptb_application = (
    Application.builder().token(settings.VVVAS_TELEGRAM_TOKEN).updater(None).build()
)

# register handlers
ptb_application.add_handler(CommandHandler("start", start))


async def telegram(request: HttpRequest) -> HttpResponse:
    """Handle incoming Telegram updates by putting them into the `update_queue`."""
    try:
        json_message = json.loads(request.body)
    except json.decoder.JSONDecodeError as err:
        return HttpResponse(str(err))
    await ptb_application.update_queue.put(
        # Update.de_json(data=json.loads(request.body), bot=ptb_application.bot)
        Update.de_json(data=json_message, bot=ptb_application.bot)
    )
    return HttpResponse()
