import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Author, Book, Review

# Create and check models

def delete_review_by_id(id):
    review = Review.objects.get(id = id)

    author = review.reviewer_name

    review.delete()

    return f"Review by {author} was deleted"

# Run and print your queries