from django.db import models


# Create your models here.

class ArtworkGallery(models.Model):
    artist_name = models.CharField(
        max_length=100
    )
    art_name = models.CharField(
        max_length=100
    )
    rating = models.IntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
