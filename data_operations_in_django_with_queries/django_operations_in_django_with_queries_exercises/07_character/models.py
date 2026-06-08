from django.db import models

# Create your models here.

CHAR_CHOICES = [
    ('Mage', 'Mage'),
    ('Warrior', 'Warrior'),
    ('Assassin', 'Assassin'),
    ('Scout', 'Scout')
]

class Character(models.Model):
    name = models.CharField(
        max_length=100
    )
    class_name = models.CharField(
        max_length=20,
        choices=CHAR_CHOICES
    )
    level = models.PositiveIntegerField()
    strength = models.PositiveIntegerField()
    dexterity = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    hit_points = models.PositiveIntegerField()
    inventory = models.TextField()
