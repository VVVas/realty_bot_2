from django.db import models


class Message(models.Model):
    """
    Модель для сообщения.
    Сообщение будет привязано к боту, само сообщение можно менять через админку
    """
    keyword = models.CharField('Ключ', max_length=128)
    title = models.CharField('Заголовок', max_length=128)
    text = models.TextField('Текст')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ('keyword',)
