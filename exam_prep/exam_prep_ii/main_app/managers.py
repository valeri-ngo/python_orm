from django.db import models
from django.db.models import Count

class ProfileManager(models.Manager):
    def get_regular_customers(self):
        """
        SELECT
            profile.*,
            COUNT(order.id) AS orders_count
        FROM profile
        JOIN order
            ON profile.id = order.profile_id
        GROUP BY
            profile.id
        HAVING
            COUNT(order.id) > 2
        ORDER BY
            orders_count DESC;
        """
        return self.annotate(
            orders_count=Count('orders')
        ).filter(
            orders_count__gt=2
        ).order_by(
            '-orders_count'
        )