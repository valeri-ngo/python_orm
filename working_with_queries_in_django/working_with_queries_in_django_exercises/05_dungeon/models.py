from django.db import models


# Create your models here.

class Dungeon(models.Model):
    DIFFICULTY_CHOICES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    name = models.CharField(
        max_length=100
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )
    location = models.CharField(
        max_length=100
    )
    boss_name = models.CharField(
        max_length=100
    )
    recommended_level = models.PositiveIntegerField()
    boss_health = models.PositiveIntegerField()
    reward = models.TextField()

