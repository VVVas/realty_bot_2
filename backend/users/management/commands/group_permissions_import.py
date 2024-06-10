from csv import DictReader
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

DATA = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename',
                            default='auth_group_permissions.csv',
                            nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(DATA, options['filename']),
                newline='',
                encoding='utf8'
            ) as csv_file:
                reader = DictReader(csv_file)
                admin_group, _ = Group.objects.get_or_create(
                    name='Администратор'
                )
                permissions_list_id = []
                for row in reader:
                    permissions_list_id.append(row['permission_id'])
                admin_group.permissions.set(permissions_list_id)
        except FileNotFoundError:
            raise CommandError(
                'Добавьте файл auth_permissions_group.csv в директорию data'
            )
        logging.warning('Успешно загружено')
