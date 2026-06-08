from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(
        max_length=100
    )
    region = models.CharField(
        max_length=50
    )
    population = models.PositiveIntegerField()
    description = models.TextField()
    is_capital = models.BooleanField(
        default=False
    )

