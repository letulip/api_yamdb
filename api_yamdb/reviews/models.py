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


class Review(models.Model):
    pass


class Rating(models.Model):
    pass

