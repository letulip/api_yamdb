from django.db import models


class Category(models.Model):
    # name = 
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    # name =
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name


class Title(models.Model):
    # name = 
    year = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    description = models.TextField(max_length=2000, blank=True, null=True)
    # genre = 
    # category = 


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
    # author = models.ForeignKey(
    #    User,
    #    on_delete=models.CASCADE,
    #    related_name='reviews'
    # )
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
    # ждём модель User
    # author = models.ForeignKey(
    #    User,
    #    on_delete=models.CASCADE,
    #    related_name='reviews'
    # )
    text = models.TextField(
        'Текст коммента',
        help_text='Введите коммент'
    )

