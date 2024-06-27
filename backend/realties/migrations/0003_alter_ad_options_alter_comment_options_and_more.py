# Generated by Django 5.0.6 on 2024-06-27 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realties', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'ordering': ('id',), 'verbose_name': 'Объявление', 'verbose_name_plural': 'объявления'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('id',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'комментарии'},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ('id',), 'verbose_name': 'Фото', 'verbose_name_plural': 'фото'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Опубликовано'),
        ),
    ]
