from django.db import models
from django.db.models import Count

class DirectorManager(models.Manager):
    
    def get_directors_by_movies_count(self):
        """
        SELECT * FROM director
        ORDER BY
            COUNT(directed_movies) DESC,
            full_name ASC;
        """
        return self.annotate(
            movies_count=Count('directed_movies')
        ).order_by('-movies_count', 'full_name')