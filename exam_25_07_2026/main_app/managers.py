from django.db import models
from django.db.models import (
    Count,
)

class PublisherManager(models.Manager):
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
        publisher.name ASC;
    """
    
    def get_publishers_by_books_count(self):
        return self.annotate(
            books_count = Count('books')
        ).order_by(
            '-books_count',
            'name',
        )