import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Application, CommandHandler


async def start(update: Update) -> None:
    """Display a message with instructions on how to use this bot."""
    text = 'VVVas not best!'
    await update.message.reply_html(text=text)


# ptb_application = (
#     Application.builder().token(settings.VVVAS_TELEGRAM_TOKEN).updater(None).build()
# )

# ptb_application.add_handler(CommandHandler("start", start))


@csrf_exempt
async def telegram(request: HttpRequest) -> HttpResponse:
    """Handle incoming Telegram updates by putting them into the `update_queue`."""
    ptb_application = (
        Application.builder().token(settings.VVVAS_TELEGRAM_TOKEN).updater(None).build()
    )

    ptb_application.add_handler(CommandHandler("start", start))

    await ptb_application.start()

    await ptb_application.update_queue.put(
        Update.de_json(data=json.loads(request.body), bot=ptb_application.bot)
    )
    return HttpResponse()
