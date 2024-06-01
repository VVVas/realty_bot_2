import requests

TOKEN = settings.TOKEN_BOT
WEBHOOK_URL = 'https://your-domain.com/path/to/webhook/'

requests.post(
    f'https://api.telegram.org/bot{TOKEN}/setWebhook',
    json={'url': WEBHOOK_URL}
)