from django.db import models

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=200)
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
    year = models.IntegerField()
    description = models.TextField(max_length=2000, blank=True, null=True)
    genre = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='Genre', blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='Category', blank=True, null=True
    )

    def __str__(self):
        return self.name

class Rating(models.Model):
    value = models.PositiveSmallIntegerField(
        "Рейтинг",
        default=10
    )


class Review(models.Model):
    CHOICES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # AVG = Review.objects.aggregate(Avg(rating))
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    # score = models.ForeignKey(
    #    Rating,
    #    choices=CHOICES,
    #    help_text='Оцените произведение',
    #    related_name='reviews',
    #    on_delete=models.SET_NULL
    # )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='review'
    )
    # Ждём
    # title = models.ForeignKey(
    #    Title,
    #    on_delete=models.CASCADE
    # )
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
