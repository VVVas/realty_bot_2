from .handlers2 import *

from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN


class TelegramBotView(View):
    bot = Bot(token=TELEGRAM_TOKEN)

    def post(self, request, *args, **kwargs):
        update = Update.de_json(json.loads(request.body), self.bot)
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("ads", ads))
        application.add_handler(CommandHandler("filter_ad_category", filter_ad_category))
        application.add_handler(conv_handler)

        async def process_update():
            await application.process_update(update)

        application.create_task(process_update())

        return JsonResponse({"status": "ok"})
