from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

class Review(models.Model):
    description = models.CharField(
        max_length=200
    )
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(
        to='Product',
        on_delete=models.CASCADE,
        related_name='reviews'
    )