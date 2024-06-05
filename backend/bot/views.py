from .handlers2 import *
#test
from django.conf import settings

TOKEN = settings.TOKEN_BOT


class TelegramBotView(View):
    bot = Bot(token=TOKEN)

    def post(self, request, *args, **kwargs):
        update = Update.de_json(json.loads(request.body), self.bot)
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("ads", ads))
        application.add_handler(CommandHandler("filter_ad_category", filter_ad_category))
        application.add_handler(conv_handler)

        async def process_update():
            await application.process_update(update)

        application.create_task(process_update())

        return JsonResponse({"status": "ok"})
