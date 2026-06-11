from django.db import models


# Create your models here.

class Workout(models.Model):
    WORKOUT_TYPE_CHOICES = (
        ('Cardio', 'Cardio'),
        ('Strength', 'Strength'),
        ('Yoga', 'Yoga'),
        ('CrossFit', 'CrossFit'),
        ('Calisthenics', 'Calisthenics'),
    )

    name = models.CharField(
        max_length=200
    )
    workout_type = models.CharField(
        max_length=20,
        choices=WORKOUT_TYPE_CHOICES
    )
    duration = models.CharField(
        max_length=30
    )
    difficulty = models.CharField(
        max_length=50
    )
    calories_burned = models.PositiveIntegerField()
    instructor = models.CharField(
        max_length=100
    )
