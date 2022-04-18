# Generated by Django 2.2.16 on 2022-04-18 09:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220418_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='This value may contain only letters,\n                digits and @/./+/-/_ characters.', regex='^[\\w.@+-]+$'), django.core.validators.RegexValidator(message="You can't create Me username.", regex='/\x08me\x08|\x08Me\x08/gm')]),
        ),
    ]