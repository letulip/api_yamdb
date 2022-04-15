from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    USER = 1
    MODERATOR = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin')
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='email address'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message="""This value may contain only letters,
                digits and @/./+/-/_ characters."""
            ),
        ],
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    bio = models.TextField(
        blank=True,
        null=True
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        default=USER
    )

    def __str__(self) -> str:
        return self.username
