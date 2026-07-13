from django.db.models import Sum
from main_app.models import Product

def product_quantity_ordered():
    total_products_ordered = Product.objects.annotate(total_ordered_quantity=Sum('orderproduct__quantity')).exclude(total_ordered_quantity=None).order_by('-total_ordered_quantity')

    result = []

    for product in total_products_ordered:
        result.append(f"Quantity ordered of {product.name}: {product.total_ordered_quantity}")
    
    return '\n'.join(result)
