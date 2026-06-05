from django.db import models
from datetime import date

class Project(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
        )
    description = models.TextField(
        null=True,
        blank=True
    )
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    duration_in_days = models.PositiveIntegerField(
        verbose_name="Duration in Days",
        null=True,
        blank=True,
    )
    estimated_hours = models.FloatField(
        verbose_name="Estimated Hours",
        null=True,
        blank=True,
    )
    start_date = models.DateField(
        verbose_name="Start Date",
        default=date.today,
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    last_edited_on = models.DateTimeField(
        auto_now=True,
        editable=False
    )
