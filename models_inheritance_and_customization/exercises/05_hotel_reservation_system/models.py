from datetime import date, timedelta
from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Create your models here.

class Hotel(models.Model):
    name = models.CharField(
        max_length=100,
    )
    address = models.CharField(
        max_length=200,
    )

class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )
    number = models.CharField(
        max_length=100,
        unique=True,
    )
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def clean(self) -> None:
        if self.total_guests > self.capacity:
            raise ValidationError('Total guests are more than the capacity of the room')
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        return f'Room {self.number} created successfully'
    
class BaseReservation(models.Model):
    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def reservation_period(self) -> int:
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self) -> Decimal:
        total_cost = self.reservation_period() * self.room.price_per_night
        return round(total_cost, 2)
    
    def get_overlapping_reservations(self, start_date: date, end_date: date) -> QuerySet['BaseReservation']:
        return self.__class__.objects.filter(
            room = self.room,
            end_date__gte = self.start_date,
            start_date__lte = self.end_date,
        )
    
    @property
    def is_available(self) -> bool:
        return not self.get_overlapping_reservations(self.start_date, self.end_date).exists()
    
    def clean(self) -> None:
        if self.start_date >= self.end_date:
            raise ValidationError('Start date cannot be after or in the same end date')
        
        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")
        
    @property
    def reservation_type(self) -> str:
        raise NotImplemented
        
    def save(self, *args, **kwargs) -> str:
        self.clean()
        super().save(*args, **kwargs)
        return f'{self.reservation_type} reservation for room {self.room.number}'

    class Meta:
        abstract = True

class RegularReservation(BaseReservation):
    
    @property
    def reservation_type(self) -> str:
        return 'Regular'

class SpecialReservation(BaseReservation):
    
    @property
    def reservation_type(self) -> str:
        return 'Special'
    
    def extend_reservation(self, days: int) -> str:
        new_end_date = self.end_date + timedelta(days=days)
        reservations = self.get_overlapping_reservations(self.start_date, new_end_date)

        if reservations:
            raise ValidationError('Error during extending reservation')
        
        self.end_date = new_end_date
        self.save()

        return f'Extended reservation for room {self.room.number} with {days} days'