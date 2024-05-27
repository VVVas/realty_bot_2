from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from realties.models import Ad


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


class Favorite(models.Model):
    """
    Модель избранного.
    favorite_ad - можно получить объявления, добавленные юзером в избранное.
    favorite_users - можно получить юзеров, добавивших объявление в избранное.
    """
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='favorite_ad',
    #     verbose_name='Пользователь',
    # ) Здесь будет связь с юзером
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='favorite_users',
        verbose_name='Объявление',
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'ad'],
                name='unique_user_ad')
        ]
