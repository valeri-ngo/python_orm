from django.db import models

class EventRegistration(models.Model):
    event_name = models.CharField(
        max_length=60
    )
    participant_name = models.CharField(
        max_length=50
    )
    registration_date = models.DateField()

    def __str__(self):
        return f"{self.participant_name} - {self.event_name}"

