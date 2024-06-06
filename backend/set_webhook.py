import requests
from django.conf import settings


TELEGRAM_TOKEN = '7186459956:AAEVCKeGIyQvlG3t4MEvxgt1nSzic3k7-7k'
WEBHOOK_URL = 'https://pb.vvvas.ru/webhook/'

requests.post(
    f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook',
    json={'url': WEBHOOK_URL}
)
