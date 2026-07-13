from decimal import Decimal

from django.db import models
from django.db.models import (
    Count,
)

# Create your models here.

class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str):
        return self.filter(
            property_type=property_type
        )

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        return self.filter(
            price__gte=min_price,
            price__lte=max_price
        )

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(
            bedrooms=bedrooms_count
        )

    def popular_locations(self):
        locations = (
            self.values('location')
            .annotate(
                location_count=Count('id')
            ).order_by(
                '-location_count'
            )[:2]
        )

        return sorted(
            locations,
            key=lambda x: x['location']
        )

class RealEstateListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Villa', 'Villa'),
        ('Cottage', 'Cottage'),
        ('Studio', 'Studio'),
    ]

    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    objects = RealEstateListingManager()