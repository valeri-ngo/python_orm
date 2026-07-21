from django.db import models
from django.db.models import Count


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self):
        """
        SELECT
            author.*,
            COUNT(a_a.article_id) AS article_count
        FROM author
        LEFT JOIN article_authors AS a_a
            ON author.id = a_a.author_id
        GROUP BY
            author.id
        ORDER BY
            article_count DESC,
            email ASC;
        """

        return self.annotate(
            article_count = Count('articles')
        ).order_by(
            '-article_count',
            'email'
        )