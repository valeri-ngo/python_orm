import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import (
    Author,
    Article,
    Review,
)
from django.db.models import (
    Count,
    Avg,
    Q,
    F,
)

# Create queries within functions

def get_authors(search_name=None, search_email=None):
    """
    SELECT
        full_name,
        email
    FROM author
    WHERE full_name ILIKE "%search_name%"
        AND email ILIKE "%search_email%"
    ORDER BY
        full_name DESC
    ;
    """

    if search_name is None and search_email is None:
        return ""
    
    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(
            Q(full_name__icontains = search_name) &
            Q(email__icontains = search_email)
        )
    elif search_name is not None:
        authors = Author.objects.filter(
            Q(full_name__icontains = search_name)
        )
    else:
        authors = Author.objects.filter(
            Q(email__icontains = search_email)
        )

    authors = authors.order_by(
        '-full_name',
    )

    return "\n".join(
        f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}"
        for a in authors
    )


def get_top_publisher():

    """
    SELECT
        author*,
        COUNT(article.id) AS count_articles
    FROM author
    LEFT JOIN article_authors
        ON author.id = article_authors.author_id
    LEFT JOIN article
        ON article.id = article_authors.article_id
    GROUP BY
        author.id
    ORDER BY
        count_articles DESC,
        author.email ASC
    LIMIT 1;
    """

    author = Author.objects.annotate(
        count_articles = Count('articles')
    ).order_by(
        '-count_articles',
        'email'
    ).first()

    if not author or author.count_articles == 0:
        return ""
    
    return (
        f"Top Author: {author.full_name} with {author.count_articles} published articles.")


def get_top_reviewer():
    
    """
    SELECT
        author*,
        COUNT(r.id) AS count_reviews
    FROM author
    LEFT JOIN review AS r
        ON author.id = r.author_id
    GROUP BY
        author.id
    ORDER BY
        count_reviews DESC,
        author.email ASC
    LIMIT 1;
    """

    author = Author.objects.annotate(
        count_reviews = Count('reviews')
    ).order_by(
        '-count_reviews',
        'email',
    ).first()

    if not author or author.count_reviews == 0:
        return ""
    
    return f"Top Reviewer: {author.full_name} with {author.count_reviews} published reviews."


def get_latest_article():
    """
    SELECT
        article.*,
        COUNT(review.id) AS num_reviews,
        AVG(review.rating) AS avg_reviews_rating
    FROM article
    LEFT JOIN review
        ON article.id = review.article_id
    LEFT JOIN article_authors AS aa
        ON article.id = aa.article_id
    LEFT JOIN author
        ON aa.author_id = author.id
    GROUP BY
        article.id
    ORDER BY
        article.published_on DESC
    LIMIT 1;
    """

    article = Article.objects.annotate(
        num_reviews = Count('reviews'),
        avg_reviews_rating = Avg('reviews__rating')
    ).order_by(
        '-published_on',
    ).first()

    if not article:
        return ""

    authors = article.authors.all().order_by('full_name')
    
    authors_name = ", ".join(a.full_name for a in authors)

    return (f"The latest article is: {article.title}. "
            f"Authors: {authors_name}. "
            f"Reviewed: {article.num_reviews} times. "
            f"Average Rating: {article.avg_reviews_rating:.2f}.")


def get_top_rated_article():

    """
    SELECT
        article.*,
        AVG(review.rating) AS avg_rating,
        COUNT(review.id) AS num_reviews
    FROM article
    JOIN review
        ON article.id = review.article_id
    GROUP BY article.id
    ORDER BY
        avg_rating DESC,
        article.title ASC
    LIMIT 1;
    """
    
    article = Article.objects.annotate(
        num_reviews = Count('reviews'),
        avg_rating = Avg('reviews__rating')
    ).order_by(
        '-avg_rating',
        'title',
    ).first()

    if not article:
        return ""
    
    return f"The top-rated article is: {article.title}, with an average rating of {article.avg_rating:.2f}, reviewed {article.num_reviews} times."


def ban_author(email=None):
    """
    SELECT
        author*
    FROM author
    WHERE email = 'email';

    UPDATE author
    SET is_banned = TRUE
    WHERE email = 'email';
    """

    if email is None:
        return "No authors banned."

    author = Author.objects.filter(
        email = email
    ).first()

    if not author:
        return "No authors banned."
    
    num_reviews = author.reviews.all().count()

    author.reviews.all().delete()

    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."