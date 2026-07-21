from decimal import Decimal
import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import (
    Profile,
    Product,
    Order,
)
from django.db.models import (
    Q,
    F,
    Count,
)

# Create queries within functions

# def populate_db():

#     profile1 = Profile.objects.create(
#         full_name = 'Adam Smith',
#         email = 'adam.smith@example.com',
#         phone_number = '123456789',
#         address = '123 Main St, Springfield',
#     )

#     profile2 = Profile.objects.create(
#         full_name = 'Susan James',
#         email = 'susan.james@example.com',
#         phone_number = '987654321',
#         address = '456 Elm St, Metropolis',
#     )

#     product1 = Product.objects.create(
#         name = 'Desk M',
#         description = 'A medium-sized office desk',
#         price = 150.00,
#         in_stock = 10,
#     )

#     product2 = Product.objects.create(
#         name = 'Display DL',
#         description = 'A 24-inch HD display',
#         price = 200.00,
#         in_stock = 5,
#     )

#     product3 = Product.objects.create(
#         name = 'Printer Br PM',
#         description = 'A high-speed printer',
#         price = 300.00,
#         in_stock = 3,
#     )

#     order1 = Order.objects.create(
#         profile = profile1,
#         total_price = 350.00,
#     )

#     order1.products.add(
#         product1,
#         product2,
#     )

#     order2 = Order.objects.create(
#         profile = profile1,
#         total_price = 300.00,
#         is_completed = True,
#     )

#     order2.products.add(
#         product3,
#     )

#     order3 = Order.objects.create(
#         profile = profile1,
#         total_price = 650.00,
#     )

#     order3.products.add(
#         product1,
#         product2,
#         product3,
#     )

#     order4 = Order.objects.create(
#         profile = profile2,
#         total_price = 450.00
#     )

#     order4.products.add(
#         product1,
#         product3,
#     )

# populate_db()

def get_profiles(search_string=None):

    """
    SELECT
        full_name,
        email,
        phone_number
    FROM profile
    WHERE 
        full_name ILIKE "%search_string%"
        OR email ILIKE "%search_string%"
        OR phone_number ILIKE "%search_string%"
    ;
    """

    if not search_string:
        return ""

    profiles = Profile.objects.annotate(
        num_of_orders = Count('orders')
    ).filter(
        Q(full_name__icontains = search_string) |
        Q(email__icontains = search_string) |
        Q(phone_number__icontains = search_string)
    ).order_by(
        'full_name'
    )

    if not profiles.exists():
        return ""
    
    return "\n".join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.num_of_orders}" for p in profiles
    )
    


def get_loyal_profiles():

    """
    SELECT
        profile.*,
        COUNT("order".id) AS count_of_orders
    FROM profile
    LEFT OUTER JOIN "order"
        ON profile.id = "order".profile_id
    GROUP BY profile.id
    HAVING COUNT("order".id) > 2
    ORDER BY count_of_orders DESC;
    """

    profiles = Profile.objects.annotate(
        count_of_orders = Count('orders')
    ).filter(
        count_of_orders__gt=2
    ).order_by(
        '-count_of_orders'
    )

    if not profiles:
        return ""
    
    return "\n".join(
        f"Profile: {p.full_name}, orders: {p.count_of_orders}" for p in profiles
    )


def get_last_sold_products():
    
    """
    SELECT
        product.*
    FROM product
    JOIN order_products
        ON product.id = order_products.product_id
    JOIN "order"
        ON "order".id = order_products.order_id
    WHERE "order".id = (
        SELECT id
        FROM "order"
        ORDER BY creation_date DESC
        LIMIT 1
    )
    ORDER BY product.name ASC;
    """

    order = Order.objects.last()

    if not order:
        return ""
    
    products = order.products.all().order_by('name')

    result = ", ".join(
        p.name for p in products
    )

    return f"Last sold products: {result}"


def get_top_products():
    """
    SELECT
        product.name,
        COUNT(order_products.order_id) AS sold_count
    FROM product
    JOIN main_app_order_products AS order_products
        ON product.id = order_products.product_id
    GROUP BY product.id, product.name
    ORDER BY sold_count DESC, product.name ASC
    LIMIT 5;
    """

    products = Product.objects.annotate(
        sold_count = Count('orders')
    ).order_by(
        '-sold_count',
        'name'
    )[:5]

    if not products:
        return ""
    
    result = (f"{p.name}, sold {p.sold_count} times" for p in products)

    return f"Top products:\n" + "\n".join(result)

def apply_discounts():

    """
    UPDATE "order"
    SET total_price = total_price * 0.9
    WHERE id IN (
        SELECT o.id
        FROM "order" o
        LEFT JOIN order_products op
            ON o.id = op.order_id
        WHERE o.is_completed = FALSE
        GROUP BY o.id
        HAVING COUNT(op.product_id) > 2
    );
    """

    orders = Order.objects.annotate(
        products_count = Count('products')
    ).filter(products_count__gt = 2,
             is_completed = False
    )

    updated_orders = orders.update(
        total_price = F('total_price') * Decimal('0.9')
    )

    return f"Discount applied to {updated_orders} orders."

def complete_order():

    order = Order.objects.filter(
        is_completed = False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ""
    
    products = order.products.all()

    for p in products:
        p.in_stock -= 1

        if p.in_stock <= 0:
            p.is_available = False

        p.save()

    order.is_completed = True
    order.save()

    return f'Order has been completed!'

# print(Profile.objects.get_regular_customers())
# print('================================================')
# print(get_profiles('Co'))
# print('================================================')
# print(get_profiles('9zz'))
# print('================================================')
# print(get_loyal_profiles())
# print('================================================')
# print(get_last_sold_products())
# print('================================================')
# print(get_top_products())
# print('================================================')
# print(apply_discounts())
# print('================================================')
# print(complete_order())