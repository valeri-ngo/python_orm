from django.db.models import (
    Sum,
    Prefetch,
    Q,
    F,
    )
from main_app.models import (
    Product,
    Order,
    OrderProduct,
    Category,
    ProductManager,
    Customer,
    )

def filter_products():
    products = Product.objects.filter(
        is_available=True,
        price__gt=3.00
    ).order_by(
        '-price',
        'name'
    )

    result = []

    for product in products:
        result.append(
            f"{product.name}: {product.price}lv."
        )

    return "\n".join(result)