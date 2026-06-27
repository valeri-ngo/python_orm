import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Product, Review
from django.db.models import Avg

# Create queries within functions

def calculate_average_rating_for_product_by_name(product_name: str):
    return Product.objects.get(name = product_name).reviews.aggregate(Avg('rating'))['rating__avg']

def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte = threshold)

def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull = True).order_by('-name')

def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull = True).delete()

# Print