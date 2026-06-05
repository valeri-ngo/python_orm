from django.db import models
    
class Course(models.Model):
    title = models.CharField(
        max_length=90
    )
    lecturer = models.CharField(
        max_length=90
    )
    description = models.TextField(
        max_length=200
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    start_date = models.DateField(
        auto_now_add=True
    )
    is_published = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.title} - {self.lecturer}"
