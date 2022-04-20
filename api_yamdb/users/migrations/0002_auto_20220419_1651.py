# Generated by Django 2.2.16 on 2022-04-19 16:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='This value may contain only letters,\n                digits and @/./+/-/_ characters.', regex='^[\\w.@+-_]+$'), django.core.validators.RegexValidator(inverse_match=True, message='Username Me registration not allowed.', regex='^\\b(m|M)e\\b')]),
        ),
    ]
