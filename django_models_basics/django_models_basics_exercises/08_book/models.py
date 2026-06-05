from django.db import models

class Book(models.Model):
    FICTION = 'Fiction'
    NON_FICTION = 'Non-Fiction'
    SCIENCE_FICTION = 'Science Fiction'
    HORROR = 'Horror'

    GENRE_CHOICES = [
        (FICTION, FICTION),
        (NON_FICTION, NON_FICTION),
        (SCIENCE_FICTION, SCIENCE_FICTION),
        (HORROR, HORROR),
    ]

    title = models.CharField(
        max_length=30
    )

    author = models.CharField(
        max_length=100
    )

    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES
    )

    publication_date = models.DateField(
        editable=False,
        auto_now_add=True
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    is_available = models.BooleanField(
        default=True
    )

    rating = models.FloatField()

    description = models.TextField()

    def __str__(self):
        return self.title
