import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Dungeon

# Create and check models
#Exercise-05 Dungeon
def show_hard_dungeons():
    dungeons = Dungeon.objects.filter(difficulty = 'Hard').order_by('-location')

    for dungeon in dungeons:
        return f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!"
    
def bulk_create_dungeons(args):
    Dungeon.objects.bulk_create(args)

def update_dungeon_names():
    Dungeon.objects.filter(difficulty = 'Easy').update(name = 'The Erased Thombs')

    Dungeon.objects.filter(difficulty = 'Medium').update(name = 'The Coral Labyrinth')

    Dungeon.objects.filter(difficulty = 'Hard').update(name = 'The Lost Haunt')

def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty = 'Easy').update(boss_health = 500)

def update_dungeon_recommended_levels():
    Dungeon.objects.filter(difficulty = 'Easy').update(recommended_level = 25)

    Dungeon.objects.filter(difficulty = 'Medium').update(recommended_level = 50)

    Dungeon.objects.filter(difficulty = 'Hard').update(recommended_level = 75)

def update_dungeon_rewards():
    Dungeon.objects.filter(boss_health = 500).update(reward = '1000 Gold')

    Dungeon.objects.filter(location__startswith = 'E').update(reward = 'New dungeon unlocked')

    Dungeon.objects.filter(location__endswith = 's').update(reward = 'Dragonheart Amulet')

def set_new_locations():
    Dungeon.objects.filter(recommended_level = 25).update(location = 'Enchanted Maze')

    Dungeon.objects.filter(recommended_level = 50).update(location = 'Grimstone Mines')

    Dungeon.objects.filter(recommended_level = 75).update(location = 'Shadowed Abyss')

# Run and print your queries
