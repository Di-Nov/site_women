# Generated by Django 4.2.1 on 2023-10-28 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='womenmodel',
            options={'ordering': ['-time_created']},
        ),
        migrations.AddField(
            model_name='womenmodel',
            name='slug',
            field=models.SlugField(default='', verbose_name='slug'),
        ),
        migrations.AddIndex(
            model_name='womenmodel',
            index=models.Index(fields=['-time_created'], name='women_women_time_cr_f62d65_idx'),
        ),
    ]
