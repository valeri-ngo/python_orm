from django.contrib import admin
from main_app.models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'director',
        'release_year',
        'genre',
    )
    list_filter = (
        'release_year',
        'genre',
    )
    search_fields = (
        'title',
        'director',
    )
