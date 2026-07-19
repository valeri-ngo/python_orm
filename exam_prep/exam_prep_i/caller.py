import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import (
    Count,
    Avg,
    F
)
from main_app.models import (
    Director,
    Actor,
    Movie,
)

# Create queries within functions

def populate_db():
    director1 = Director.objects.create(
        full_name = 'Francis Ford Coppola',
        birth_date = '1939-04-07',
        nationality = 'Unknown',
        years_of_experience = 50,
    )

    director2 = Director.objects.create(
        full_name = 'Akira Kurosawa',
        birth_date = '1910-03-23',
        nationality = 'Unknown',
        years_of_experience = 0,
    )

    director3 = Director.objects.create(
        full_name = 'Martin Scorsese',
        birth_date = '1942-11-17',
        nationality = 'American and Italian',
        years_of_experience = 60,
    )

    actor1 = Actor.objects.create(
        full_name = 'Al Pacino',
        birth_date = '1940-04-25',
        nationality = 'American',
        is_awarded = True,
    )

    actor2 = Actor.objects.create(
        full_name = 'Robert Duvall',
        birth_date = '1931-01-05',
        nationality = 'American',
        is_awarded = False,
    )

    actor3 = Actor.objects.create(
        full_name = 'Joaquin Phoenix',
        birth_date = '1974-10-28',
        nationality = 'American',
        is_awarded = True,
    )

    movie1 = Movie.objects.create(
        title = 'The Godfather',
        release_date = '1972-03-24',
        storyline = 'The aging patriarch of an organized crime dynasty transfers control to his reluctant son.',
        genre = 'Drama',
        rating = 9.9,
        is_classic = True,
        is_awarded = True,
        director = director1,
        starring_actor = actor1,
    )

    movie1.actors.add(actor1, actor2)

    movie2 = Movie.objects.create(
        title = 'Apocalypse Now',
        release_date = '1979-08-15',
        storyline = 'A journey upriver to confront a rogue colonel.',
        genre = 'Drama',
        rating = 9.1,
        director = director1,
        starring_actor = actor1,
    )

    movie2.actors.add(actor1, actor2)

    movie3 = Movie.objects.create(
        title = 'Seven Samurai',
        release_date = '1954-04-26',
        storyline = 'Villagers hire samurai to protect them from bandits.',
        genre = 'Action',
        rating = 8.6,
        is_classic = True,
        is_awarded = True,
        director = director2,
        starring_actor = actor3,
    )

    movie3.actors.add(actor3)

populate_db()

def get_directors(search_name=None, search_nationality=None):

    """
    SELECT * FROM director
    WHERE full_name ILIKE '%search_name%'
        AND nationality ILIKE '%search_nationality%'
    ORDER BY full_name ASC;
    """

    if search_name and search_nationality:
        directors = Director.objects.filter(
            full_name__icontains=search_name,
            nationality__icontains=search_nationality
        )
    
    elif search_name:
        directors = Director.objects.filter(
            full_name__icontains=search_name
        )

    elif search_nationality:
        directors = Director.objects.filter(
            nationality__icontains=search_nationality
        )
    
    else:
        return ""
    
    directors = directors.order_by('full_name')

    return "\n".join(
        f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}" for d in directors
    )

def get_top_director():

    """
    SELECT
        director.*,
        COUNT(movie.id) AS movies_count
    FROM director
    LEFT JOIN movie
        ON director.id = movie.director_id
    GROUP BY director.id
    ORDER BY
        movies_count DESC,
        full_name ASC;
    """

    directors = Director.objects.get_directors_by_movies_count()

    top_director = directors.first()

    if top_director is None:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.movies_count}."

def get_top_actor():

    """
    SELECT
        actor.id,
        actor.full_name,
        COUNT(movie.id) AS movies_count,
        AVG(movie.rating) AS avg_rating
    FROM actor
    JOIN movie_actors
    ON actor.id = movie_actors.actor_id
    JOIN movie
    ON movie.id = movie_actors.movie_id
    GROUP BY actor.id, actor.full_name
    ORDER BY movies_count DESC, actor.full_name ASC
    LIMIT 1;
    """

    top_actor = Actor.objects.annotate(
        movies_count=Count('starring_movies'),
        movies_avg_rating=Avg('starring_movies__rating'),
    ).filter(
        movies_count__gt=0
    ).order_by(
        '-movies_count',
        'full_name'
    ).first()

    if top_actor is None:
        return ""

    movie_titles = ", ".join(
        top_actor.starring_movies.values_list(
            'title',
            flat=True
        )
    )

    return (
        f"Top Actor: {top_actor.full_name}, "
        f"starring in movies: {movie_titles}, "
        f"movies average rating: {top_actor.movies_avg_rating:.1f}"
    )

def get_actors_by_movies_count():

    """
    SELECT
        actor.id,
        actor.full_name,
        COUNT(movie.id) AS movies_count
    FROM actor
    JOIN movie_actors
        ON actor.id = movie_actors.actor_id
    JOIN movie
        ON movie.id = movie_actors.movie_id
    GROUP BY
        actor.id,
        actor.full_name
    ORDER BY
        movies_count DESC,
        actor.full_name ASC
    LIMIT 3;
    """

    top_actors = Actor.objects.annotate(
        movies_count = Count('movies')
    ).filter(
        movies_count__gt=0
    ).order_by(
        '-movies_count',
        'full_name'
    )[:3]
    
    if not top_actors:
        return ""
    
    return "\n".join(
        f"{actor.full_name}, participated in {actor.movies_count} movies"
        for actor in top_actors
    )

def get_top_rated_awarded_movie():

    """
    SELECT
        id,
        title,
        rating
    FROM movie
    WHERE is_awarded=True
    ORDER BY
        rating DESC,
        title ASC
    LIMIT 1;
    """

    movie = Movie.objects.filter(
        is_awarded=True
    ).order_by(
        '-rating',
        'title'
    ).first()

    if movie is None:
        return ""

    starring_actor = (
        movie.starring_actor.full_name
        if movie.starring_actor
        else "N/A"
    )

    cast = ", ".join(
        movie.actors
        .order_by("full_name")
        .values_list("full_name", flat=True)
    )

    return (
        f"Top rated awarded movie: {movie.title}, "
        f"rating: {movie.rating:.1f}. "
        f"Starring actor: {starring_actor}. "
        f"Cast: {cast}."
    )

def increase_rating():

    """
    SELECT
        *
    FROM movie
    WHERE
        is_classic = TRUE
        AND rating < 10;
    UPDATE movie
    SET rating = rating + 0.1
    WHERE
        is_classic = TRUE
        AND rating < 10;
    """

    num_of_updated_movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10
    ).update(
        rating=F('rating') + 0.1
    )

    if num_of_updated_movies == 0:
        return "No ratings increased."
    
    return f"Rating increased for {num_of_updated_movies} movies."

print(Director.objects.get_directors_by_movies_count())
print()
print(get_directors(search_name='S', search_nationality=None))
print()
print(get_directors(search_name='Martin', search_nationality='Canadian'))
print()
print(get_top_director())
print()
print(get_top_actor())
print()
print(get_actors_by_movies_count())
print()
print(get_top_rated_awarded_movie())
print()
print(increase_rating())
print()
print(increase_rating())