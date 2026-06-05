from django.db import models
     
class Student(models.Model):
    first_name = models.CharField(
        max_length=50
    )
    last_name = models.CharField(
        max_length=50
    )
    age = models.PositiveIntegerField()
    grade = models.CharField(
        max_length=10
    )
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
