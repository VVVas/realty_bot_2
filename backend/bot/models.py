from django.db import models


class BotMessage(models.Model):
    """
    Модель для сообщения.
    Сообщение будет привязано к боту, само сообщение можно менять через админку
    """
    keyword = models.CharField(
        'Ключ', unique=True, max_length=128,
        verbose_name='Ключ', verbose_name_plural='Ключи')
    title = models.CharField('Заголовок', max_length=128,
                             verbose_name='Заголовок', verbose_name_plural='Заголовоки')
    text = models.TextField('Текст',
                            verbose_name='Текст', verbose_name_plural='Тексты')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('keyword',)
