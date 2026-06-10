import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models

def find_books_by_genre_and_language(book_genre, book_language):
    find_books = Book.objects.filter(genre = book_genre, language = book_language)
    
    return find_books

# Run and print your queries
