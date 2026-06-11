import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Workout

# Create and check models
#Lab-06 Workout
def show_workouts():
    workouts = Workout.objects.filter(workout_type__in = ['Calisthenics', 'CrossFit']).order_by('id')

    result = []

    for workout in workouts:
        result.append(f"{workout.name} from {workout.workout_type} type has {workout.difficulty} difficulty!")

    return '\n'.join(result)

def get_high_difficulty_cardio_workouts():
    filtered_workouts = Workout.objects.filter(workout_type = 'Cardio', difficulty = 'High').order_by('instructor')

    return filtered_workouts

def set_new_instructors():
    workouts = Workout.objects.all()

    for workout in workouts:
        if workout.workout_type == 'Cardio':
            workout.instructor = 'John Smith'

        elif workout.workout_type == 'Strength':
            workout.instructor = 'Michael Williams'

        elif workout.workout_type == 'Yoga':
            workout.instructor = 'Emily Johnson'

        elif workout.workout_type == 'CrossFit':
            workout.instructor = 'Sarah Davis'
        
        elif workout.workout_type == 'Calisthenics':
            workout.instructor = 'Chris Heria'

        workout.save()

def set_new_duration_times():
    workouts = Workout.objects.all()

    for workout in workouts:
        if workout.instructor == 'John Smith':
            workout.duration = '15 minutes'

        elif workout.instructor == 'Sarah Davis':
            workout.duration = '30 minutes'

        elif workout.instructor == 'Chris Heria':
            workout.duration = '45 minutes'

        elif workout.instructor == 'Michael Williams':
            workout.duration = '1 hour'

        elif workout.instructor == 'Emily Johnson':
            workout.duration = '1 hour and 30 minutes'

        workout.save()

def delete_workouts():
    Workout.objects.exclude(workout_type__in = ['Strength', 'Calisthenics']).delete()

# Run and print your queries
