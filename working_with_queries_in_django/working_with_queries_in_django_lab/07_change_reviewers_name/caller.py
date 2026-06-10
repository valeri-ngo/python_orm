import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models

def change_reviewer_name(rev_name, new_name):
    Review.objects.filter(reviewer_name = rev_name).update(reviewer_name = new_name)

    return Review.objects.all()

# Run and print your queries
