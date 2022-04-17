# Generated by Django 2.2.16 on 2022-04-16 18:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='value',
            field=models.PositiveSmallIntegerField(default=10, verbose_name='Рейтинг'),
        ),
        migrations.AddField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='text',
            field=models.TextField(default=(2015, 10, 9, 23, 55, 59, 342380), help_text='Введите текст отзыва', verbose_name='Текст отзыва'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите коммент', verbose_name='Текст коммента')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Review')),
            ],
        ),
    ]