from django.db import models

# Create your models here.

class Car(models.Model):
    model = models.CharField(
        max_length=40
    )
    year = models.PositiveIntegerField()
    color = models.CharField(
        max_length=40
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    price_with_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

