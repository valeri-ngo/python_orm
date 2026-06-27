import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Owner
from main_app.models import Car
from main_app.models import Registration
from datetime import date

# Create queries within functions

def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull = True).first()
    car = Car.objects.filter(registration__isnull = True).first()

    if car is None or registration is None:
        return None
    
    car.owner = owner
    car.save()
    
    registration.car = car
    registration.registration_date = date.today()
    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

# Print
