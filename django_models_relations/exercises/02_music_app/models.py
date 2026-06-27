from django.db import models

# Create your models here.

class Song(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True
    )

class Artist(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    songs = models.ManyToManyField(
        to='Song',
        related_name='artists'
    )