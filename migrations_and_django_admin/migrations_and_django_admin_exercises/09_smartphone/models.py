from django.db import models

class Smartphone(models.Model):
    brand = models.CharField(
        max_length=100
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    category = models.CharField(
        max_length=20,
        default='No category'
    )
