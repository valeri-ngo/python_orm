from django.db.models import Avg, Count, Manager
from main_app.querysets import RealEstateListingQuerySet,VideoGameQuerySet

class RealEstateListingManager(Manager.from_queryset(RealEstateListingQuerySet)):

    def popular_locations(self) -> dict:
        """
        SELECT 
            location,
            COUNT(location) AS location_count
        FROM
            real_estate_listing
        GROUP BY
            location
        ORDER BY
            location_count DESC,
            location ASC
        LIMIT 2;
        """
        return self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]
    
class VideoGameManager(Manager.from_queryset(VideoGameQuerySet)):
    
    def highest_rated_game(self) -> 'VideoGame':
        """
        SELECT * FROM video_game
        ORDER BY rating DESC
        LIMIT 1;
        """
        return self.order_by('-rating').first()

    def lowest_rated_game(self) -> 'VideoGame':
        return self.order_by('rating').first()
    
    def average_rating(self) -> str:
        """
        SELECT AVG('rating') AS avg_rating
        FROM video_game;
        """
        avg_rating = self.aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        return f"{avg_rating:.1f}"
    