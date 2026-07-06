from decimal import Decimal

from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(
        max_length=100
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def calculate_tax(self):
        return self.price * Decimal('0.08')
    
    def calculate_shipping_cost(self, weight: Decimal):
        return weight * Decimal('2.00')
    
    def format_product_name(self):
        return f"Product: {self.name}"

class DiscountedProduct(Product):

    def calculate_price_without_discount(self):
        return self.price * Decimal('1.20')
    
    def calculate_tax(self):
        return self.price * Decimal('0.05')
    
    def calculate_shipping_cost(self, weight: Decimal):
        return weight * Decimal('1.50')
    
    def format_product_name(self):
        return f"Discounted Product: {self.name}"
    
    class Meta:
        proxy = True