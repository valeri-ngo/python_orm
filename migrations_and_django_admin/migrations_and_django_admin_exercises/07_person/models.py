from django.db import models
  
class Person(models.Model):
    name = models.CharField(
        max_length=40
    )
    age = models.PositiveIntegerField()
    age_group = models.CharField(
        max_length=20,
        default='No age group'
    )

    def __str__(self):
        return f"Name: {self.name}"
