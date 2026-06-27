from django.db import models

# Create your models here.

class Driver(models.Model):
    first_name = models.CharField(
        max_length=50
    )
    last_name = models.CharField(
        max_length=50
    )

class DrivingLicense(models.Model):
    license_number = models.CharField(
        max_length=10,
        unique=True
    )
    issue_date = models.DateField()
    driver = models.OneToOneField(
        'Driver',
        on_delete=models.CASCADE,
        related_name='license'
    )