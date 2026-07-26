from django.db import models
from django.db.models import (
    Count,
)


class AstronautManager(models.Manager):
    """
    SELECT
        astronaut.*,
        COUNT(mission_astronaut.mission_id) AS missions_count
    FROM astronaut
    LEFT JOIN mission_astronaut
        ON astronaut.id = mission_astronaut.astronaut_id
    GROUP BY astronaut.id
    ORDER BY
        missions_count DESC,
        phone_number ASC;
    """

    def get_astronauts_by_missions_count(self):
        return self.annotate(
            missions_count = Count('missions')
        ).order_by(
            '-missions_count',
            'phone_number'
        )