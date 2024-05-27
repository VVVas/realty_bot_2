from django.db import models

from users.models import Profile


class Category(models.Model):
    """Модель категории объявления."""
    title = models.CharField(
        'Название', max_length=32, null=False
    )

    class Meta:
        ordering = ('title',)


class City(models.Model):
    """Модель города."""
    title = models.CharField(
        'Название', max_length=16, null=False
    )
    timezone = models.CharField(
        'Часовой пояс (от Москвы)', max_length=3, null=True
    )

    class Meta:
        ordering = ('title',)


class RealtyAd(models.Model):
    """Модель торгового центра/склада."""
    title = models.CharField(
        'Название торогового центра/склада', max_length=128, null=True
    )
    management_company = models.CharField(
        'Название управляющей компании', max_length=128, null=True
    )
    phone_number = models.CharField(
        'Номер стационарного телефона', max_length=16, null=True
    )
    mobile_number = models.CharField(
        'Номер мобильного телефона', max_length=16, null=True
    )
    address = models.CharField(
        'Адрес', max_length=256, null=False
    )
    email = models.EmailField(
        'Электронная почта', max_length=32, null=True
    )
    website = models.CharField(
        'Сайт', max_length=32, null=True
    )
    contact_name = models.CharField(
        'Контактное лицо', max_length=32, null=True
    )
    city = models.OneToOneField(
        'Город', City, on_delete=models.DO_NOTHING
    )
    category = models.ForeignKey(
        'Категория', Category, on_delete=models.DO_NOTHING
    )
    img = models.FileField(
        'Фото', null=True
    )

    class Meta:
        verbose_name = 'Торговый центры'
        verbose_name_plural = 'торговые центры'
        ordering = ('title',)


class Ad(models.Model):
    """Модель объявлений"""
    title = models.CharField(
        'Название объявления', max_length=128, null=True
    )
    realty_place = models.ForeignKey(
        'Место, в котором выставлено объвление', RealtyAd,
        on_delete=models.DO_NOTHING
    )
    address = models.CharField(
        'Точный адрес объявления',
        max_length=256, null=False
    )
    additional_information = models.TextField(
        'Дополнительная информация',
    )


class Photo(models.Model):
    """Модель фотографии к объявлению."""
    date_create = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    img = models.FileField(
        'Фото', null=True
    )
    ad = models.ForeignKey(
        'Фотография для объявления',
        Ad, on_delete=models.CASCADE, related_name='photos', null=True
    )
    user = models.ForeignKey(
        'Связь с моделью юзера',
        Profile, on_delete=models.DO_NOTHING, related_name='photos'
    )


class Comment(models.Model):
    """Модель комментария к объявлению."""
    date_create = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    text = models.TextField(
        'Текст объявления', null=False
    )
    ad = models.ForeignKey(
        'Связь с моделью объявления',
        Ad, on_delete=models.CASCADE, related_name='comment', null=True
    )
    user = models.ForeignKey(
        'Связь с моделью юзера',
        Profile, on_delete=models.DO_NOTHING, related_name='comment'
    )
