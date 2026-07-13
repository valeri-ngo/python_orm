from decimal import Decimal

from main_app.models import (
    Product,
    )

def give_discount():

    products = Product.objects.filter(
        is_available=True,
        price__gt=3.00
    ).order_by(
        '-price',
        'name'
    )

    result = []

    for product in products:
        product.price *= Decimal('0.70')
        result.append(
            f"{product.name}: {product.price:.2f}lv."
        )

    return "\n".join(result)