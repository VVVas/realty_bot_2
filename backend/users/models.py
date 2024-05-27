from django.db import models

from realties.models import Ad


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
