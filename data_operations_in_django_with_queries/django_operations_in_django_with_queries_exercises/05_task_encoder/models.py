from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(
        max_length=25
    )
    description = models.TextField()
    due_date = models.DateField()
    is_finished = models.BooleanField(
        default=False
    )

