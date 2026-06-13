import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Workout

# Create and check models
#Exercise-06 Workout
def show_workouts():
    Workout.objects.filter(workout_type__in = ['Calisthenics', 'CrossFit']).order_by('id')

    result = []

    for workout in Workout.objects.order_by('id'):
        result.append(f"{workout.name} from {workout.workout_type} type has {workout.difficulty} difficulty!")

    return '\n'.join(result)
    
def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(workout_type = 'Cardio', difficulty = 'High').order_by('instructor')

def set_new_instructors():
    Workout.objects.filter(workout_type = 'Cardio').update(instructor = 'John Smith')

    Workout.objects.filter(workout_type = 'Strength').update(instructor = 'Michael Williams')

    Workout.objects.filter(workout_type = 'Yoga').update(instructor = 'Emily Johnson')

    Workout.objects.filter(workout_type = 'CrossFit').update(instructor = 'Sarah Davis')

    Workout.objects.filter(workout_type = 'Calisthenics').update(instructor = 'Chris Heria')

def set_new_duration_times():
    Workout.objects.filter(instructor = 'John Smith').update(duration = '15 minutes')

    Workout.objects.filter(instructor = 'Sarah Davis').update(duration = '30 minutes')

    Workout.objects.filter(instructor = 'Chris Heria').update(duration = '45 minutes')

    Workout.objects.filter(instructor = 'Michael Williams').update(duration = '1 hour')

    Workout.objects.filter(instructor = 'Emily Johnson').update(duration = '1 hour and 30 minutes')

def delete_workouts():
    Workout.objects.exclude(workout_type__in = ['Strength', 'Calisthenics']).delete()

# Run and print your queries
