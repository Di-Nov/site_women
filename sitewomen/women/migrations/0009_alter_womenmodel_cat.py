# Generated by Django 4.2.1 on 2023-11-03 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0008_husband_m_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='womenmodel',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cat_post', to='women.category'),
        ),
    ]