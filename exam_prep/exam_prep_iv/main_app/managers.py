from django.db import models
from django.db.models import Count


class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self):

        """
        SELECT
            tennisplayer.*,
            COUNT(match.id) AS wins_count
        FROM tennisplayer
        LEFT JOIN matche
            ON tennisplayer.id = match.winner_id
        GROUP BY
            tennisplayer.id
        ORDER BY
            wins_count DESC,
            tennisplayer.full_name ASC
        """

        return self.annotate(
            wins_count = Count('won_matches')
        ).order_by(
            '-wins_count',
            'full_name'
        )