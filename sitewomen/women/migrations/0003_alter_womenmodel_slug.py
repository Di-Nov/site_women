# Generated by Django 4.2.1 on 2023-10-28 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0002_alter_womenmodel_options_womenmodel_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='womenmodel',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
    ]
