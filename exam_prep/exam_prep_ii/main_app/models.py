from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
)
from main_app.managers import ProfileManager

# Create your models here.

class TimeStampedMixin(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True

class Profile(TimeStampedMixin, models.Model):
    full_name = models.CharField(
        max_length=100,
        help_text='Represents the full name of the user.',
        validators=[MinLengthValidator(2)],
    )
    email = models.EmailField(
        help_text='Represents the email address of the user.',
    )
    phone_number = models.CharField(
        max_length=15,
        help_text='This field is typically a string to accommodate various phone number formats.',
    )
    address = models.TextField(
        help_text='This field can store longer text, suitable for addresses.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Indicates whether the profile is active or not.',
    )
    objects = ProfileManager()

    def __str__(self):
        return self.full_name


class Product(TimeStampedMixin, models.Model):
    name = models.CharField(
        max_length=100,
        help_text='Represents the name of the product.',
    )
    description = models.TextField(
        help_text='Provides a detailed description of the product.',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='Represents the price of the product.',
    )
    in_stock = models.PositiveIntegerField(
        help_text='Represents the quantity of the product in stock.',
    )
    is_available = models.BooleanField(
        help_text='Indicates whether the product is currently available for purchase.',
        default=True,
    )

    def __str__(self):
        return self.name


class Order(TimeStampedMixin, models.Model):
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    products = models.ManyToManyField(
        'Product',
        related_name='orders'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text='Represents the total price of the order.',
    )
    is_completed = models.BooleanField(
        default=False,
        help_text='Indicates whether the order has been completed or not.',
    )

    def __str__(self):
        return f"Order #{self.id}"