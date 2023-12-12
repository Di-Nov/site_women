# Generated by Django 4.2.1 on 2023-12-11 14:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0010_alter_category_options_alter_womenmodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='womenmodel',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photo/%Y/%m/%d', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='womenmodel',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.MaxLengthValidator(255, message='Максимум 100 символов'), django.core.validators.MinLengthValidator(3, 'Минимум 3 символов')], verbose_name='Слаг'),
        ),
    ]
