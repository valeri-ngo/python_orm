from datetime import date

from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(
        max_length=50
    )
    last_name = models.CharField(
        max_length=50
    )
    phone_number = models.CharField(
        max_length=10
    )

    class Meta:
        abstract = True

class ZooKeeper(Employee):

    SPEC_CHOICES = (
        ('Mammals', 'Mammals'),
        ('Birds', 'Birds'),
        ('Reptiles', 'Reptiles'),
        ('Others', 'Others'),
    )

    specialty = models.CharField(
        max_length=10,
        choices=SPEC_CHOICES
    )
    managed_animals = models.ManyToManyField(
        to='Animal'
    )

    def clean(self):
        
        choices = [choice[0] for choice in self.SPEC_CHOICES]

        if self.specialty not in choices:
            raise ValidationError('Specialty must be a valid choice.')

