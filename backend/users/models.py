from django.contrib.auth.models import AbstractUser
from django.db import models

from . import constants


class User(AbstractUser):

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'администраторы'
        ordering = ('username',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
    STATUS_CHOICES = (
        (constants.STATUS_ACTIVE, 'Активный'),
        (constants.STATUS_READONLY, 'Только чтение'),
        (constants.STATUS_BLOCKED, 'Заблокирован'),
    )
    external_id = models.PositiveBigIntegerField(
        'ID пользователя в Телеграм',
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя', max_length=255, blank=True, null=True
    )
    first_name = models.CharField(
        'Имя', max_length=255,
    )
    last_name = models.CharField(
        'Фамилия', max_length=255, blank=True, null=True
    )
    date = models.DateTimeField(
        'Дата регистрации', auto_now_add=True
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=255,
        choices=STATUS_CHOICES,
        default=constants.STATUS_ACTIVE
    )

    class Meta:
        verbose_name = 'Профиль телеграм'
        verbose_name_plural = 'профили телеграм'

    def __str__(self):
        return f'{self.external_id} - {self.first_name} {self.last_name}'

    @property
    def is_active(self):
        return self.status == constants.STATUS_ACTIVE

    @property
    def is_readonly(self):
        return self.status == constants.STATUS_READONLY

    @property
    def is_blocked(self):
        return self.status == constants.STATUS_BLOCKED

    @classmethod
    def get_default_tg_user_profile(cls):
        tg_user_profile, _ = Profile.objects.get_or_create(
            first_name='Unknown', external_id='1',
            status=constants.STATUS_BLOCKED,
        )
        return tg_user_profile.pk

    @staticmethod
    def delete_profile_and_comments(user):
        user.comment.filter(user=user).delete()
        user.photos.filter(user=user).delete()
        user.save()
        user.delete()
