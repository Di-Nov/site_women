# Generated by Django 4.2.1 on 2023-10-31 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0005_tagpost_womenmodel_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='womenmodel',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=1),
        ),
    ]
