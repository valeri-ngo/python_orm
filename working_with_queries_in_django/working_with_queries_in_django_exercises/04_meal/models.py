from django.db import models


# Create your models here.

class Meal(models.Model):
    MEAL_TYPE_CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snack', 'Snack'),
    )

    name = models.CharField(
        max_length=100
    )
    meal_type = models.CharField(
        max_length=10,
        choices=MEAL_TYPE_CHOICES
    )
    preparation_time = models.CharField(
        max_length=30
    )
    difficulty = models.PositiveIntegerField()
    calories = models.PositiveIntegerField()
    chef = models.CharField(
        max_length=100
    )

