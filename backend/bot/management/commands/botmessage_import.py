from csv import DictReader
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bot.models import BotMessage

DATA = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='botmessage.csv', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(DATA, options['filename']),
                newline='',
                encoding='utf8'
            ) as csv_file:
                reader = DictReader(csv_file)
                for row in reader:
                    if BotMessage.objects.filter(
                        keyword=row['keyword']
                    ).exists():
                        continue
                    _, created = BotMessage.objects.get_or_create(**row)
        except FileNotFoundError:
            raise CommandError(
                'Добавьте файл botmessage.csv в директорию data'
            )
        logging.warning('Успешно загружено')
