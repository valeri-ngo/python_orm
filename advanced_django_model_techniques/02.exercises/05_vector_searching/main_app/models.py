from django.db import models
from django.contrib.postgres.search import SearchVectorField

# Create your models here.

class Document(models.Model):
    title = models.CharField(
        max_length=200
    )
    content = models.TextField()
    search_vector = SearchVectorField(
        null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['search_vector'])
        ]