from django.db import models


# Create your models here.
#Laptop
class Laptop(models.Model):
    BRAND_CHOICES = (
        ('Asus', 'Asus'),
        ('Acer', 'Acer'),
        ('Apple', 'Apple'),
        ('Lenovo', 'Lenovo'),
        ('Dell', 'Dell'),
    )
    
    OS_CHOICES = (
        ('Windows', 'Windows'),
        ('MacOS', 'MacOS'),
        ('Linux', 'Linux'),
        ('ChromeOS', 'ChromeOS'),
    )

    brand = models.CharField(
        max_length=20,
        choices=BRAND_CHOICES
    )
    processor = models.CharField(
        max_length=100
    )
    memory = models.PositiveIntegerField(
        help_text='Memory in GB'
    )
    storage = models.PositiveIntegerField(
        help_text='Storage in GB'
    )
    operation_system = models.CharField(
        max_length= 20,
        choices=OS_CHOICES
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
