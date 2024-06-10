import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission

# from realty.settings import ADMIN_PERMISSIONS

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
            admin_group, _ = Group.objects.get_or_create(
                name='Администратор'
            )
            permissions_list_id = []
            for codename in settings.ADMIN_PERMISSIONS:
                permissions_list_id.append(
                    Permission.objects.get(codename=codename).id
                )
            admin_group.permissions.set(permissions_list_id)
        except CommandError:
            raise CommandError(
                'Ошибка загрузки прав'
            )
        logging.warning('Успешно загружено')
