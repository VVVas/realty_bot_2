from django.db import models


class BotMessage(models.Model):
    """
    Модель для сообщения.
    Сообщение будет привязано к боту, само сообщение можно менять через админку
    """
    keyword = models.CharField(
        unique=True, max_length=128,
        verbose_name='Ключ'
    )
    title = models.CharField(
        max_length=128,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('keyword',)
