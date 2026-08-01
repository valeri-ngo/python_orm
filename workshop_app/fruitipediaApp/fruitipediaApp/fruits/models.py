from django.db import models
from django.core.validators import MinLengthValidator
from .validators import is_string_validator


# Create your models here.

class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        validators=[
            MinLengthValidator(2),
        ],
    )
    image_url = models.URLField(
        null=False,
        blank=False,
    )
    description = models.TextField(
        null=False,
        blank=False,
    )
    nutrition = models.TextField(
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='fruits',
    )