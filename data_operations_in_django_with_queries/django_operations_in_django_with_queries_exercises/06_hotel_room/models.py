from django.db import models

# Create your models here.

HOTELROOM_CHOICES = [
    ('Standard', 'Standard'),
    ('Deluxe', 'Deluxe'),
    ('Suite', 'Suite')
]

class HotelRoom(models.Model):
    room_number = models.PositiveIntegerField()
    room_type = models.CharField(
        max_length=10,
        choices=HOTELROOM_CHOICES
    )
    capacity = models.PositiveIntegerField()
    amenities = models.TextField()
    price_per_night = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    is_reserved = models.BooleanField(
        default = False
    )
