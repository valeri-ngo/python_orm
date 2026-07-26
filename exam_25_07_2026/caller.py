from decimal import Decimal
import os
import django
from django.db.models import (
    F,
    Q,
    Case,
    Count,
    Avg,
    Value,
    When,
)

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import (
    Publisher,
    Author,
    Book,
)

# Create queries within functions

# Django Queries I

def get_publishers(search_string=None):
    """
    SELECT
        name,
        country,
        rating
    FROM publisher
    WHERE
        name ILIKE '%search_string%'
        OR country ILIKE '%search_string%'
    ORDER BY
        rating DESC,
        name ASC;
    """

    if search_string is None:
        return 'No search criteria.'

    publishers = Publisher.objects.filter(
        Q(name__icontains = search_string) |
        Q(country__icontains = search_string)
    ).order_by(
        '-rating',
        'name',
    )

    if not publishers.exists():
        return 'No publishers found.'

    return "\n".join(
        f"Publisher: {p.name}, "
        f"country: {'Unknown' if p.country == 'TBC' else p.country}, "
        f"rating: {p.rating:.1f}"
    for p in publishers
    )

def get_top_publisher():
    """
    SELECT
        publisher.*,
        COUNT(book.id) AS books_count
    FROM publisher
    LEFT JOIN book
        ON publisher.id = book.publisher_id
    GROUP BY publisher.id
    ORDER BY
        books_count DESC,
        publisher.name ASC
    LIMIT 1;
    """

    publisher = Publisher.objects.get_publishers_by_books_count().first()

    if not publisher:
        return "No publishers found."

    return f"Top Publisher: {publisher.name} with {publisher.books_count} books."

def get_top_main_author():
    """
    SELECT
        author.*,
        COUNT(book.id) AS books_count,
        AVG(book.rating) AS books_avg_rating
    FROM author
    LEFT JOIN book
        ON author.id = book.main_author_id
    GROUP BY
        author.id
    ORDER BY
        books_count DESC,
        author.name ASC
    LIMIT 1;
    """
    author = Author.objects.annotate(
        books_count = Count('books'),
        books_avg_rating = Avg('books__rating')
    ).order_by(
        '-books_count',
        'name',
    ).first()

    if not author or author.books_count == 0:
        return 'No results.'

    titles = author.books.order_by(
        'title',
    ).values_list(
        'title',
        flat=True,
    )

    return (
        f"Top Author: {author.name}, "
        f"own book titles: {', '.join(titles)}, "
        f"books average rating: {author.books_avg_rating:.1f}"
    )


# Django Queries II

def get_authors_by_books_count():
    """
    SELECT
        a.*,
        COUNT(DISTINCT b.id) + COUNT(DISTINCT bc.book_id) AS books_count
    FROM author AS a
    LEFT JOIN book AS b
        ON a.id = b.main_author_id
    LEFT JOIN book_co_authors AS bc
        ON a.id = bc.author_id
    GROUP BY
        a.id
    ORDER BY
        books_count DESC,
        a.name ASC
    LIMIT 3;
    """

    authors = Author.objects.annotate(
        books_count=Count('books',distinct=True) +
         Count('co_authors_books',distinct=True)
    ).order_by(
        '-books_count',
        'name',
    )[:3]

    if not authors.exists() or authors.first().books_count == 0:
        return "No results."

    return "\n".join(
        f"{a.name} authored {a.books_count} books."
        for a in authors
    )

def get_bestseller():
    """
    SELECT
        book.*,
        COUNT(book_co_authors.author_id) AS co_authors_count,
        book.rating + COUNT(book_co_authors.author_id) + 1 AS idx
    FROM book
    LEFT JOIN book_co_authors
        ON book.id = book_co_authors.book_id
    WHERE book.is_bestseller = TRUE
    GROUP BY book.id
    ORDER BY
        idx DESC,
        book.rating DESC,
        co_authors_count DESC,
        book.title ASC
    LIMIT 1;
    """
    
    bestseller = (
        Book.objects
        .filter(is_bestseller=True)
        .select_related("main_author")
        .prefetch_related("co_authors")
        .annotate(
            co_authors_count=Count("co_authors", distinct=True)
        )
        .annotate(
            idx=F("rating") + F("co_authors_count") + Value(1)
        )
        .order_by(
            "-idx",
            "-rating",
            "-co_authors_count",
            "title",
        )
        .first()
    )

    if not bestseller:
        return 'No results.'

    co_authors = bestseller.co_authors.order_by("name")

    if co_authors.exists():
        names = "/".join(a.name for a in co_authors)
    else:
        names = "N/A"

    return (
    f"Top bestseller: {bestseller.title}, "
    f"index: {bestseller.idx:.1f}. "
    f"Main author: {bestseller.main_author.name}. "
    f"Co-authors: {names}."
    )

def increase_price():
    """
UPDATE book
    SET price =
        CASE
            WHEN price > 50
                THEN price * 1.10
            ELSE
                price * 1.20
        END
    FROM publisher
    WHERE
        book.publisher_id = publisher.id
        AND EXTRACT(YEAR FROM publication_date) = 2025
        AND (book.rating + publisher.rating) >= 8.0;
    """
    
    books = Book.objects.annotate(
        total_rating=F("rating") + F("publisher__rating")
    ).filter(
        publication_date__year=2025,
        total_rating__gte=8,
    )

    updated_books = books.update(
        price=Case(
            When(price__gt=50, then=F("price") * Decimal('1.10')),
            default=F("price") * Decimal('1.20'),
        )
    )

    if updated_books == 0:
        return "No changes in price."

    return f"Prices increased for {updated_books} book/s."

# def populate_db():

#     # Creating publishers

#     publisher1 = Publisher.objects.create(
#         name = 'Epic Reads',
#         country = 'U.S.',
#         established_date = '1923-05-15',
#         rating = 4.94,
#     )
#     publisher2 = Publisher.objects.create(
#         name = 'Global Prints',
#         country = 'Australia',
#     )
#     publisher3 = Publisher.objects.create(
#         name = 'Abrams Books',
#         rating = 1.05,
#     )

#     # Creating authors

#     author1 = Author.objects.create(
#         name = 'Jack London',
#         country = 'U.S.',
#         birth_date = '1876-01-12',
#         is_active = False,
#     )
#     author2 = Author.objects.create(
#         name = 'Craig Richardson',
#     )
#     author3 = Author.objects.create(
#         name = 'Ramsey Hamilton',
#     )
#     author4 = Author.objects.create(
#         name = 'Luciano Ramalho',
#     )

#     # Creating books

#     book1 = Book.objects.create(
#         title = 'Adventures in Python',
#         publication_date = '2015-06-01',
#         summary = 'An engaging and detailed guide to mastering a popular programming language.',
#         genre = 'Non-Fiction',
#         price = 49.99,
#         rating = 4.8,
#         publisher = publisher1,
#         main_author = author2,
#     )
#     book1.co_authors.add(author3)

#     book2 = Book.objects.create(
#         title='The Call of the Wild',
#         publication_date='1903-11-23',
#         summary='A classic fiction adventure story set during the Klondike Gold Rush.',
#         genre='Fiction',
#         price=29.99,
#         rating=4.9,
#         is_bestseller=True,
#         publisher=publisher2,
#         main_author=author1,
#     )

#     book3 = Book.objects.create(
#         title='Django World',
#         publication_date='2025-01-01',
#         summary='A comprehensive resource for advanced users of a web development framework.',
#         genre='Non-Fiction',
#         price=90.00,
#         rating=5.0,
#         publisher=publisher1,
#         main_author=author2,
#     )

#     book3.co_authors.add(author4, author3)

#     book4 = Book.objects.create(
#         title='Integration Testing',
#         publication_date='2024-12-31',
#         summary='A thorough exploration of expert-level testing strategies.',
#         genre='Non-Fiction',
#         price=89.99,
#         rating=4.89,
#         is_bestseller=True,
#         publisher=publisher1,
#         main_author=author3,
#     )


#     book5 = Book.objects.create(
#         title='Unit Testing',
#         publication_date='2025-02-01',
#         summary='A detailed guide to foundational testing principles.',
#         genre='Non-Fiction',
#         price=50.00,
#         rating=3.99,
#         publisher=publisher1,
#         main_author=author2,
#     )

#     book5.co_authors.add(author3)

# populate_db()

# print(Publisher.objects.get_publishers_by_books_count())
# print('======================================================================================')
# print(get_publishers(search_string='p'))
# print('======================================================================================')
# print(get_publishers(search_string=''))
# print('======================================================================================')
# print(get_publishers(search_string=None))
# print('======================================================================================')
# print(get_publishers(search_string='z'))
# print('======================================================================================')
# print(get_top_publisher())
# print('======================================================================================')
# print(get_top_main_author())
# print('======================================================================================')
# print(get_authors_by_books_count())
# print('======================================================================================')
# print(get_bestseller())
# print('======================================================================================')
# print(increase_price())
# print('======================================================================================')
