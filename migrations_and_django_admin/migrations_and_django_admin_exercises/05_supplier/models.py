from django.db import models
      
class Supplier(models.Model):
    name = models.CharField(
        max_length=100
    )
    contact_name = models.CharField(
        max_length=50
    )
    email = models.EmailField(
        unique=True
    )
    phone = models.CharField(
        max_length=20,
        unique=True
    )
    address = models.TextField(
        max_length=254
    )

    def __str__(self):
        return f"{self.name} - {self.phone}"
