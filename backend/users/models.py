from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
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
    is_active = models.BooleanField(
        'Активный', default=True,
    )
    date_joined = models.DateTimeField(
        'Дата регистрации', default=timezone.now
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return f'{self.external_id} - {self.first_name} {self.last_name}'
