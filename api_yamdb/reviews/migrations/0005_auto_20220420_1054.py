# Generated by Django 2.2.16 on 2022-04-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220420_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.CharField(choices=[(1, 'один'), (2, 'два'), (3, 'три'), (4, 'четыре'), (5, 'пять'), (6, 'шесть'), (7, 'семь'), (8, 'восемь'), (9, 'девять'), (10, 'десять')], help_text='Оцените произведение', max_length=10),
        ),
    ]