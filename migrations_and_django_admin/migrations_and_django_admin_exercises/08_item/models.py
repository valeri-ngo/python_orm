from django.db import models
    
class Item(models.Model):
    name = models.CharField(
        max_length=100
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    quantity = models.PositiveIntegerField(
        default=1
    )
    rarity = models.CharField(
        max_length=20,
        default='No rarity'
    )
