from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class BaseMedia(models.Model):
    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    genre = models.CharField(
        max_length=50
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(5, message='Author must be at least 5 characters long')
        ]
    )
    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(6, message='ISBN must be at least 6 characters long')
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'

class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(8, message='Director must be at least 8 characters long')
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'

class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(9, message='Artist must be at least 9 characters long')
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'