from django.db import models


# Create your models here.

class ChessPlayer(models.Model):
    username = models.CharField(
        max_length=100,
        unique=True
    )
    title = models.CharField(
        max_length=100,
        default="no title"
    )
    rating = models.PositiveIntegerField(
        default=1500
    )
    games_played = models.PositiveIntegerField(
        default=0
    )
    games_won = models.PositiveIntegerField(
        default=0
    )
    games_lost = models.PositiveIntegerField(
        default=0
    )
    games_drawn = models.PositiveIntegerField(
        default=0
    )

