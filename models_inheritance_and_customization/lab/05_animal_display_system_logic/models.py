from datetime import date

from django.db import models

# Create your models here.

class Animal(models.Model):
    name = models.CharField(
        max_length=100
    )
    species = models.CharField(
        max_length=100
    )
    birth_date = models.DateField()
    sound = models.CharField(
        max_length=100
    )

class Mammal(Animal):
    fur_color = models.CharField(
        max_length=50
    )

class Bird(Animal):
    wing_span = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

class Reptile(Animal):
    scale_type = models.CharField(
        max_length=50
    )

class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."

    def is_endangered(self):
        endangered = ['Cross River Gorilla', 'Orangutan', 'Green Turtle']

        if self.species in endangered:
            return f'{self.species} is at risk!'
        else:
            return f'{self.species} is not at risk.'

