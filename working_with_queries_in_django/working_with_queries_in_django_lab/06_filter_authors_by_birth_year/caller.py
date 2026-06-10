import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models

def filter_authors_by_birth_year(year1, year2):
    authors_year = Author.objects.filter(
        birth_date__year__gte = year1,
        birth_date__year__lte = year2)\
            .order_by('-birth_date')

    result = []

    for author in authors_year:
        result.append(
            f"{author.birth_date}: "
            f"{author.first_name} {author.last_name}"
            )
    
    return '\n'.join(result)

# Run and print your queries

