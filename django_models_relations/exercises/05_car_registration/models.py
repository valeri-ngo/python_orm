from django.db import models

# Create your models here.

class Owner(models.Model):
    name = models.CharField(
        max_length=50
    )

class Car(models.Model):
    model = models.CharField(
        max_length=50
    )
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(
        to='Owner',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cars'
    )

class Registration(models.Model):
    registration_number = models.CharField(
        max_length=10,
        unique=True
    )
    registration_date = models.DateField(
        null=True,
        blank=True
    )
    car = models.OneToOneField(
        to='Car',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='registration'
    )