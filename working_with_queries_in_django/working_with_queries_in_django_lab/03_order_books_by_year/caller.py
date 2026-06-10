import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models

def order_books_by_year():
    ordered_books = Book.objects.order_by('publication_year', 'title')

    result = []

    for books in ordered_books:
        result.append(f"{books.publication_year} year: {books.title} by {books.author}")

    return '\n'.join(result)

# Run and print your queries