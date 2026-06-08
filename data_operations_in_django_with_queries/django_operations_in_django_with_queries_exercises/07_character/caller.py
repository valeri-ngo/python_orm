import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Character

# Create queries within functions

def update_characters():
    chars = Character.objects.all()

    for char in chars:

        if char.class_name == 'Mage':
            char.level += 3
            char.intelligence -= 7
        
        elif char.class_name == 'Warrior':
            char.hit_points //= 2
            char.dexterity += 4

        elif char.class_name == 'Scout' \
            or char.class_name == 'Assassin':
            char.inventory = 'The inventory is empty'

        char.save()

def fuse_characters(first_character: Character, second_character: Character):
    if first_character.class_name in ['Mage', 'Scout']:
        
        inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    
    elif first_character.class_name in ['Warrior', 'Assassin']:
        
        inventory = 'Dragon Scale Armor, Excalibur'

    name = f"{first_character.name} {second_character.name}"
    class_name = 'Fusion'
    level = (first_character.level + second_character.level) // 2
    strength = int((first_character.strength + second_character.strength) * 1.2)
    dexterity = int((first_character.dexterity + second_character.dexterity) * 1.4)
    intelligence = int((first_character.intelligence + second_character.intelligence) * 1.5)
    hit_points = (first_character.hit_points + second_character.hit_points)

    fused_char = Character.objects.create(
        name = name,
        class_name = class_name,
        level = level,
        strength = strength,
        dexterity = dexterity,
        intelligence = intelligence,
        hit_points = hit_points,
        inventory = inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity():
    chars = Character.objects.all()

    for char in chars:
        char.dexterity += 30

        char.save()

def grand_intelligence():
    chars = Character.objects.all()

    for char in chars:
        char.intelligence += 40

        char.save()

def grand_strength():
    chars = Character.objects.all()

    for char in chars:
        char.strength += 50

        char.save()

def delete_characters():
    chars = Character.objects.all()

    for char in chars:
        if char.inventory == 'The inventory is empty':
            char.delete()

character1 = Character.objects.create(
    name='Gandalf',
    class_name='Mage',
    level=10,
    strength=15,
    dexterity=20,
    intelligence=25,
    hit_points=100,
    inventory='Staff of Magic, Spellbook',
)

character2 = Character.objects.create(
    name='Hector',
    class_name='Warrior',
    level=12,
    strength=30,
    dexterity=15,
    intelligence=10,
    hit_points=150,
    inventory='Sword of Troy, Shield of Protection',
)

fuse_characters(character1, character2)
fusion = Character.objects.filter(class_name='Fusion').get()

print(fusion.name)
print(fusion.class_name)
print(fusion.level)
print(fusion.intelligence)
print(fusion.inventory)