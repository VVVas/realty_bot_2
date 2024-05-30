from django.db import models

from users.models import Profile


class Category(models.Model):
    """Модель категории недвижимости."""
    title = models.CharField(
        'Название', max_length=32,
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
        'Название', max_length=32,
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

    @classmethod
    def get_default_city_pk(cls):
        city, _ = City.objects.get_or_create(title='Unknown')
        return city.pk


class Realty(models.Model):
    """Модель недвижимости."""
    title = models.CharField(
        'Название недвижимости', max_length=128, blank=True, null=True,
    )
    phone_number = models.TextField(
        'Номер стационарного телефона', blank=True, null=True
    )
    mobile_number = models.TextField(
        'Номер мобильного телефона', blank=True, null=True
    )
    number = models.TextField(
        'Номер бесплатной линии 8800', blank=True, null=True
    )
    address = models.CharField(
        'Адрес', max_length=256, blank=True, null=True
    )
    email = models.TextField(
        'Электронная почта', blank=True, null=True
    )
    site = models.TextField(
        'Сайт', blank=True, null=True
    )
    contact_name = models.TextField(
        'Контактное лицо', blank=True, null=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_DEFAULT,
        default=City.get_default_city_pk,
        verbose_name='Город',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        blank=True, null=True,
    )
    img = models.FileField(
        'Фото', blank=True, null=True, upload_to='images/'
    )
    additional_information = models.TextField(
        'Дополнительная информация',
        blank=True, null=True,
    )

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'недвижимость'
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title


class Ad(models.Model):
    """Модель объявлений"""
    title = models.CharField(
        'Название объявления', max_length=128
    )
    realty = models.ForeignKey(
        Realty,
        on_delete=models.PROTECT,
        verbose_name='Объект',
    )
    address = models.CharField(
        'Точный адрес объявления',
        max_length=256
    )
    additional_information = models.TextField(
        'Дополнительная информация',
        blank=True, null=True
    )
    date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'объявления'

    def __str__(self) -> str:
        return self.title


class Photo(models.Model):
    """Модель фотографии к объявлению."""
    date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    img = models.FileField(
        'Фото', null=True
    )
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name='photos',
        verbose_name='Объявление'
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.SET_DEFAULT,
        default=Profile.get_default_tg_user_profile,
        related_name='photos',
        verbose_name='Пользователь'
    )
    is_published = models.BooleanField(
        'Премодерация админом', default=False
    )

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'фото'


class Comment(models.Model):
    """Модель комментария к объявлению."""
    date_create = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    text = models.TextField('Текст комментария')
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Объявление'
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.SET_DEFAULT,
        default=Profile.get_default_tg_user_profile,
        related_name='comment',
        verbose_name='Пользователь'
    )
    is_published = models.BooleanField(
        'Премодерация админом', default=False
    )

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
