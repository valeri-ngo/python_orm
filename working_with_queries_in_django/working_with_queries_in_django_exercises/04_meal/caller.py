import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Meal

# Create and check models
#Exercise-04 Meal
def set_new_chefs():
    Meal.objects.filter(meal_type = 'Breakfast').update(chef = 'Gordon Ramsay')

    Meal.objects.filter(meal_type = 'Lunch').update(chef = 'Julia Child')

    Meal.objects.filter(meal_type = 'Dinner').update(chef = 'Jamie Oliver')

    Meal.objects.filter(meal_type = 'Snack').update(chef = 'Thomas Keller')

def set_new_preparation_times():
    Meal.objects.filter(meal_type = 'Breakfast').update(preparation_time = '10 minutes')

    Meal.objects.filter(meal_type = 'Lunch').update(preparation_time = '12 minutes')

    Meal.objects.filter(meal_type = 'Dinner').update(preparation_time = '15 minutes')

    Meal.objects.filter(meal_type = 'Snack').update(preparation_time = '5 minutes')

def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in = ['Breakfast', 'Dinner']).update(calories = 400)

def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in = ['Lunch', 'Snack']).update(calories = 700)

def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in = ['Lunch', 'Snack']).delete()

# Run and print your queries
