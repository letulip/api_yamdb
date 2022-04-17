from django.db import models


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

class Review(models.Model):
    pass


class Rating(models.Model):
    pass
