import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Laptop

# Create and check models

#Exercise-02 Laptop
def show_the_most_expensive_laptop():
    laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"

def bulk_create_laptops(args):
    Laptop.objects.bulk_create(args)

def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in = ['Asus', 'Lenovo']).update(storage = 512)

def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in = ['Apple', 'Dell', 'Acer']).update(memory = 16)

def update_operation_systems():
    Laptop.objects.filter(brand = 'Asus').update(operation_system= 'Windows')
    
    Laptop.objects.filter(brand = 'Apple').update(operation_system= 'MacOS')

    Laptop.objects.filter(brand__in = ['Dell', 'Acer']).update(operation_system= 'Linux')

    Laptop.objects.filter(brand = 'Lenovo').update(operation_system= 'Chrome OS')

def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt = 1200).delete()

# Run and print your queries
