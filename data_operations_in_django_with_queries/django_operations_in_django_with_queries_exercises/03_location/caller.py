import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Location

# Create queries within functions

Location.objects.create(
    name = 'Sofia',
    region = 'Sofia Region',
    population = 1329000,
    description = 'The capital of Bulgaria and the largest city in the country',
    is_capital = False
)

Location.objects.create(
    name = 'Plovdiv',
    region = 'Plovdiv Region',
    population = 346942,
    description = 'The second-largest city in Bulgaria with a rich historical heritage',
    is_capital = False
)

Location.objects.create(
    name = 'Varna',
    region = 'Varna Region',
    population = 330486,
    description = 'A city known for its sea breeze and beautiful beaches on the Black Sea',
    is_capital = False
)

def show_all_locations():
    ordered_locations = Location.objects.all().order_by('-id')

    locations = []

    for location in ordered_locations:
        locations.append(
            f"{location.name} has a population of {location.population}!"
        )

    return '\n'.join(locations)

def new_capital():
    location = Location.objects.first()

    if location:
        location.is_capital = True
        location.save()

def get_capitals():
    return Location.objects.filter(is_capital = True).values('name')

def delete_first_location():
    deleted_location = Location.objects.first()

    if deleted_location:
        deleted_location.delete()

print(show_all_locations())
print(new_capital())
print(get_capitals())
