import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models

def find_authors_nationalities():
    found_authors = Author.objects.exclude(nationality = None)

    result = []

    for author in found_authors:
        result.append(f"{author.first_name} {author.last_name} is {author.nationality}")

    return '\n'.join(result)

# Run and print your queries