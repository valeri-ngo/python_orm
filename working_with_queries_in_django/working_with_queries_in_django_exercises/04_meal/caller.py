import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Meal

# Create and check models
#Lab-04 Meal
def set_new_chefs():
    meals = Meal.objects.all()

    for meal in meals:
        if meal.meal_type == 'Breakfast':
            meal.chef = 'Gordon Ramsay'
        
        elif meal.meal_type == 'Lunch':
            meal.chef = 'Julia Child'
        
        elif meal.meal_type == 'Dinner':
            meal.chef = 'Jamie Oliver'

        else:
            meal.chef = 'Thomas Keller'
        
        meal.save()

def set_new_preparation_times():
    meals = Meal.objects.all()

    for meal in meals:
        if meal.meal_type == 'Breakfast':
            meal.preparation_time = '10 minutes'

        elif meal.meal_type == 'Lunch':
            meal.preparation_time = '12 minutes'

        elif meal.meal_type == 'Dinner':
            meal.preparation_time = '15 minutes'

        else:
            meal.preparation_time = '5 minutes'
        
        meal.save()

def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in = ['Breakfast', 'Dinner']).update(calories = 400)

def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in = ['Lunch', 'Snack']).update(calories = 700)

def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in = ['Lunch', 'Snack']).delete()

# Run and print your queries
