from django.db import models

class Movie(models.Model):
    title = models.CharField(
        max_length=100
    )
    director = models.CharField(
        max_length=100
    )
    release_year = models.PositiveIntegerField()
    genre = models.CharField(
        max_length=50
    )

    def __str__(self):
        return f'Movie "{self.title} by {self.director}"'
