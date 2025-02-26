# Generated by Django 5.0.6 on 2024-06-14 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название объявления')),
                ('address', models.CharField(max_length=256, verbose_name='Точный адрес объявления')),
                ('additional_information', models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Стоимость за кв. м.')),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'объявления',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'категории',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='Название')),
                ('timezone', models.CharField(help_text='Пример записи для Москвы: +3. Для Новосибирска: +7', max_length=3, null=True, verbose_name='Часовой пояс (по UTC)')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'города',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'избранное',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('img', models.FileField(null=True, upload_to='', verbose_name='Фото')),
                ('is_published', models.BooleanField(default=False, verbose_name='Премодерация админом')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'фото',
            },
        ),
        migrations.CreateModel(
            name='Realty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название недвижимости')),
                ('phone_number', models.TextField(blank=True, null=True, verbose_name='Номер стационарного телефона')),
                ('mobile_number', models.TextField(blank=True, null=True, verbose_name='Номер мобильного телефона')),
                ('number', models.TextField(blank=True, null=True, verbose_name='Номер бесплатной линии 8800')),
                ('address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Адрес')),
                ('email', models.TextField(blank=True, null=True, verbose_name='Электронная почта')),
                ('site', models.TextField(blank=True, null=True, verbose_name='Сайт')),
                ('contact_name', models.TextField(blank=True, null=True, verbose_name='Контактное лицо')),
                ('img', models.FileField(blank=True, null=True, upload_to='images/', verbose_name='Фото')),
                ('additional_information', models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')),
            ],
            options={
                'verbose_name': 'Недвижимость',
                'verbose_name_plural': 'недвижимость',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('is_published', models.BooleanField(default=False, verbose_name='Премодерация админом')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='realties.ad', verbose_name='Объявление')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'комментарии',
            },
        ),
    ]
