from django.db import models

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="titles",
        blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genre, related_name="titles", blank=True
    )


class Rating(models.Model):
    value = models.PositiveSmallIntegerField(
        "Рейтинг",
        default=10
    )


class Review(models.Model):
    CHOICES = (
        (1, 'один'),
        (2, 'два'),
        (3, 'три'),
        (4, 'четыре'),
        (5, 'пять'),
        (6, 'шесть'),
        (7, 'семь'),
        (8, 'восемь'),
        (9, 'девять'),
        (10, 'десять')
    )
    # AVG = Review.objects.aggregate(Avg(rating))
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    score = models.ForeignKey(
        Rating,
        choices=CHOICES,
        help_text='Оцените произведение',
        related_name='reviews',
        default=10,
        on_delete=models.SET_DEFAULT
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='review'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField(
        'Текст коммента',
        help_text='Введите коммент'
    )
