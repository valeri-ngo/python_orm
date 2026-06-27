from django.db import models

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

class Veterinarian(Employee):
    license_number = models.CharField(
        max_length=10
    )
