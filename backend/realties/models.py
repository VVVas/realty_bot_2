from django.db import models

from users.models import Profile


class Category(models.Model):
    """Модель категории недвижимости."""
    title = models.CharField(
        'Название', max_length=32, null=False
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> str:
        return self.title


class City(models.Model):
    """Модель города."""
    title = models.CharField(
        'Название', max_length=16, null=False
    )
    timezone = models.CharField(
        'Часовой пояс (по UTC)', max_length=3, null=True,
        help_text='Пример записи для Москвы: +3. Для Новосибирска: +7'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Город'
        verbose_name_plural = 'города'

    def __str__(self) -> str:
        return self.title


class Realty(models.Model):
    """Модель недвижимости."""
    title = models.CharField(
        'Название недвижимости', max_length=128, null=True
    )
    phone_number = models.TextField(
        'Номер стационарного телефона', null=True
    )
    mobile_number = models.TextField(
        'Номер мобильного телефона', null=True
    )
    number = models.TextField(
        'Номер бесплатной линии 8800', null=True
    )
    address = models.CharField(
        'Адрес', max_length=256, null=False
    )
    email = models.TextField(
        'Электронная почта', null=True
    )
    site = models.TextField(
        'Сайт', null=True
    )
    contact_name = models.TextField(
        'Контактное лицо', null=True
    )
    city = models.ForeignKey(
        City, on_delete=models.DO_NOTHING
    )
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING
    )
    img = models.FileField(
        'Фото', null=True, upload_to='images/'
    )
    additional_information = models.TextField(
        'Дополнительная информация',
    )

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'недвижимости'
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title


class Ad(models.Model):
    """Модель объявлений"""
    title = models.CharField(
        'Название объявления', max_length=128, null=True
    )
    realty = models.ForeignKey(
        Realty,
        on_delete=models.DO_NOTHING
    )
    address = models.CharField(
        'Точный адрес объявления',
        max_length=256, null=False
    )
    additional_information = models.TextField(
        'Дополнительная информация',
    )
    date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'объявления'


class Photo(models.Model):
    """Модель фотографии к объявлению."""
    date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    img = models.FileField(
        'Фото', null=True
    )
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='photos', null=True
    )
    user = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, related_name='photos'
    )
    is_validate = models.BooleanField('Премодерация админом')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'фото'


class Comment(models.Model):
    """Модель комментария к объявлению."""
    date_create = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    text = models.TextField(
        'Текст объявления', null=False
    )
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='comment', null=True
    )
    user = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, related_name='comment'
    )
    is_validate = models.BooleanField('Премодерация админом')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'комментарии'


class Favorite(models.Model):
    """
    Модель избранного.
    favorite_ad - можно получить объявления, добавленные юзером в избранное.
    favorite_users - можно получить юзеров, добавивших объявление в избранное.
    """
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='favorite_ad',
        verbose_name='Пользователь',
    )
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
