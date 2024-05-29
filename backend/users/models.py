from django.contrib.auth.models import AbstractUser
from django.db import models

from users import const


class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    STATUS_CHOICES = (
        (const.STATUS_ACTIVE, 'Активный'),
        (const.STATUS_READONLY, 'Только чтение'),
        (const.STATUS_BLOCKED, 'Заблокирован'),
    )
    external_id = models.PositiveIntegerField(
        'ID пользователя в Телеграм',
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя', max_length=255, blank=True
    )
    first_name = models.CharField(
        'Имя', max_length=255,
    )
    last_name = models.CharField(
        'Фамилия', max_length=255, blank=True
    )
    date = models.DateTimeField(
        'Дата регистрации', auto_now_add=True
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=STATUS_CHOICES,
        default=const.STATUS_ACTIVE
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return f'{self.external_id} - {self.first_name} {self.last_name}'

    @property
    def is_active(self):
        return self.status == const.STATUS_ACTIVE

    @property
    def is_readonly(self):
        return self.status == const.STATUS_READONLY

    @property
    def is_blocked(self):
        return self.status == const.STATUS_BLOCKED
