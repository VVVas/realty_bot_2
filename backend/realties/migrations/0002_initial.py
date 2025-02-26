# Generated by Django 5.0.6 on 2024-06-14 13:30

import django.db.models.deletion
import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('realties', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=users.models.Profile.get_default_tg_user_profile, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='comment', to='users.profile', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_users', to='realties.ad', verbose_name='Объявление'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_ad', to='users.profile', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='photo',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='realties.ad', verbose_name='Объявление'),
        ),
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(default=users.models.Profile.get_default_tg_user_profile, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='photos', to='users.profile', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='realty',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='realties', to='realties.category', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='realty',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='realties', to='realties.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='ad',
            name='realty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ads', to='realties.realty', verbose_name='Объект'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'ad'), name='unique_user_ad'),
        ),
        migrations.AddConstraint(
            model_name='realty',
            constraint=models.UniqueConstraint(fields=('title', 'city', 'address'), name='unique_title_city_address'),
        ),
    ]
