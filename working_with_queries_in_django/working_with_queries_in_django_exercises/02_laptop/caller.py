import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Laptop

# Create and check models

#Lab-02 Laptop
def show_the_most_expensive_laptop():
    laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"

def bulk_create_laptops(args: List[Laptop]):
    Laptop.objects.bulk_create(args)

def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in = ['Asus', 'Lenovo']).update(storage = 512)

def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in = ['Apple', 'Dell', 'Acer']).update(memory = 16)

def update_operation_systems():
    laptops = Laptop.objects.all()

    for laptop in laptops:
        if laptop.brand == 'Asus':
            laptop.operation_system = 'Windows'
        
        elif laptop.brand == 'Apple':
            laptop.operation_system = 'MacOS'

        elif laptop.brand in ['Dell', 'Acer']:
            laptop.operation_system = 'Linux'

        else:
            laptop.operation_system = 'Chrome OS'

        laptop.save()
        
# Run and print your queries
