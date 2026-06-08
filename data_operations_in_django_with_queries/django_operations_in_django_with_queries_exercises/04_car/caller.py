import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Car
from decimal import Decimal

# Create queries within functions

Car.objects.create(
    model = 'Mercedes C63 AMG',
    year = 2019,
    color = 'white',
    price = 120000.00
)

Car.objects.create(
    model = 'Audi Q7 S line',
    year = 2023,
    color = 'black',
    price = 183900.00
)

Car.objects.create(
    model = 'Chevrolet Corvette',
    year = 2021,
    color = 'dark grey',
    price = 199999.00
)

def apply_discount():
    
    for car in Car.objects.all():

        digits = car.year

        sum_digits = sum(int(d) for d in str(digits))

        discount = Decimal(sum_digits) / Decimal('100')

        new_price = car.price - (car.price * discount)

        car.price_with_discount = new_price
        car.save()

def get_recent_cars():
    return Car.objects.filter(year__gt = 2020).values(
        'model',
        'price_with_discount'
    )

def delete_last_car():
    last_car = Car.objects.last()

    if last_car:
        last_car.delete()

apply_discount()
print(get_recent_cars())
