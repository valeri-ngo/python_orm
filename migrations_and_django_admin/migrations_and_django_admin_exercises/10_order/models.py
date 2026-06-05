from django.db import models
  
ORDER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled')
]

class Order(models.Model):
    product_name = models.CharField(
        max_length=30
    )
    customer_name = models.CharField(
        max_length=100
    )
    order_date = models.DateField()
    status = models.CharField(
        max_length=30,
        choices=ORDER_STATUS_CHOICES
    )
    amount = models.PositiveIntegerField(
        default=1
    )
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    warranty = models.CharField(
        max_length=264,
        default='No warranty'
    )
    delivery = models.DateField(
        null=True,
        blank=True
    )
