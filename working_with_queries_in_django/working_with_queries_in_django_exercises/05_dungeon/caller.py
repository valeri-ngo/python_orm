import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Dungeon

# Create and check models
#Lab-05 Dungeon
def show_hard_dungeons():
    dungeons = Dungeon.objects.filter(difficulty = 'Hard').order_by('-location')

    result = []

    for dungeon in dungeons:
        result.append(f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!")

    return '\n'.join(result)

def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)

def update_dungeon_names():
    dungeons = Dungeon.objects.all()

    for dungeon in dungeons:
        if dungeon.difficulty == 'Easy':
            dungeon.name = 'The Erased Thombs'

        elif dungeon.difficulty == 'Medium':
            dungeon.name = 'The Coral Labyrinth'

        else:
            dungeon.name = 'The Lost Haunt'

        dungeon.save()

def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty = 'Easy').update(boss_health = 500)

def update_dungeon_recommended_levels():
    dungeons = Dungeon.objects.all()

    for dungeon in dungeons:
        if dungeon.difficulty == 'Easy':
            dungeon.recommended_level = 25
        
        elif dungeon.difficulty == 'Medium':
            dungeon.recommended_level = 50

        elif dungeon.difficulty == 'Hard':
            dungeon.recommended_level = 75

        dungeon.save()

def update_dungeon_rewards():
    dungeons = Dungeon.objects.all()

    for dungeon in dungeons:
        if dungeon.boss_health == 500:
            dungeon.reward = '1000 Gold'

        if dungeon.location.startswith('E'):
            dungeon.reward = 'New dungeon unlocked'

        if dungeon.location.endswith('s'):
            dungeon.reward = 'Dragonheart Amulet'

        dungeon.save()

def set_new_locations():
    dungeons = Dungeon.objects.all()

    for dungeon in dungeons:
        if dungeon.recommended_level == 25:
            dungeon.location = 'Enchanted Maze'

        elif dungeon.recommended_level == 50:
            dungeon.location = 'Grimstone Mines'
        
        elif dungeon.recommended_level == 75:
            dungeon.location = 'Shadowed Abyss'

        dungeon.save()

# Run and print your queries
