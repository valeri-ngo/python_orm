from django.db import models

CITIES = (("Sofia", "Sofia"),
("Plovdiv", "Plovdiv"),
("Burgas", "Burgas"),
("Varna", "Varna"))

class Department(models.Model):
    code = models.CharField(
        max_length=4,
        primary_key=True,
        unique=True,
        )
    name = models.CharField(
        max_length=50,
        unique=True
        )
    employees_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Employees Count"
        )
    location = models.CharField(
        max_length=20,
        choices=CITIES,
        null=True,
        blank=True
    )
    last_edited_on = models.DateTimeField(
        auto_now=True,
        editable=False
        )

