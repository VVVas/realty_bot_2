import requests
from django.conf import settings

TELEGRAM_TOKEN = settings.TELEGRAM_TOKEN
WEBHOOK_URL = 'https://your-domain.com/path/to/webhook/'

requests.post(
    f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook',
    json={'url': WEBHOOK_URL}
)
