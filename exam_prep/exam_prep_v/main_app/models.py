from django.db import models
from django.core.validators import (
    MinValueValidator,
)
from main_app.mixins import (
    NameMixin,
    UpdatedAtMixin,
    LaunchDateMixin,
)
from main_app.validators import digits_validate
from main_app.managers import AstronautManager


# Create your models here.

class Astronaut(NameMixin, UpdatedAtMixin):
    phone_number = models.CharField(
        max_length=15,
        validators=[digits_validate],
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    spacewalks = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0),],
    )
    objects = AstronautManager()

    def __str__(self):
        return self.name

class Spacecraft(NameMixin, LaunchDateMixin, UpdatedAtMixin):
    manufacturer = models.CharField(
        max_length=100,
    )
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),],
    )
    weight = models.FloatField(
        validators=[MinValueValidator(0.0),],
    )

    def __str__(self):
        return self.name

class Mission(NameMixin, LaunchDateMixin, UpdatedAtMixin):

    STATUS_CHOICES = (
        ('Planned', 'Planned'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    )

    description = models.TextField(
        null=True,
        blank=True,
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=9,
        default='Planned',
    )
    spacecraft = models.ForeignKey(
        'Spacecraft',
        on_delete=models.CASCADE,
        related_name='missions',
    )
    astronauts = models.ManyToManyField(
        'Astronaut',
        related_name='missions',
    )
    commander = models.ForeignKey(
        'Astronaut',
        on_delete=models.SET_NULL,
        null=True,
        related_name='commanded_missions',
    )

    def __str__(self):
        return self.name
