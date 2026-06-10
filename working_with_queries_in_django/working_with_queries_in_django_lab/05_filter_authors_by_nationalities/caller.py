import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models

def filter_authors_by_nationalities(nationality):
    authors_by_nationality = Author.objects.filter(nationality = nationality).order_by('first_name', 'last_name')

    result = []

    for author in authors_by_nationality:
        if author.biography:
            result.append(f"{author.biography}")
        else:
            result.append(f"{author.first_name} {author.last_name}")
        
    return '\n'.join(result)

# Run and print your queries
