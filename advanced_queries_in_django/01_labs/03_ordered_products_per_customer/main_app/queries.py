from django.db.models import (
    Sum,
    Prefetch,
    )
from main_app.models import (
    Product,
    Order,
    OrderProduct,
    Category,
    ProductManager,
    Customer,
    )

def product_quantity_ordered():
    total_products_ordered = Product.objects.annotate(total_ordered_quantity=Sum('orderproduct__quantity')).exclude(total_ordered_quantity=None).order_by('-total_ordered_quantity')

    result = []

    for product in total_products_ordered:
        result.append(f"Quantity ordered of {product.name}: {product.total_ordered_quantity}")
    
    return '\n'.join(result)

def ordered_products_per_customer():
    orders = Order.objects.order_by(
        'id'
    ).select_related(
        'customer'
    ).prefetch_related(
        Prefetch(
            'orderproduct_set',
            queryset=OrderProduct.objects.select_related(
                'product__category'
            )
        )
    )
    result = []

    for order in orders:
        result.append(
            f"Order ID: {order.id}, Customer: {order.customer.username}"
        )

        for item in order.orderproduct_set.all():
            result.append(
                f"- Product: {item.product.name}, "
                f"Category: {item.product.category.name}"
            )

    return "\n".join(result)