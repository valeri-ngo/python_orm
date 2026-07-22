import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import (
    TennisPlayer,
    Tournament,
    Match,
)
from django.db.models import (
    Count,
    Q,
    F,
)

# Create queries within functions

def get_tennis_players(search_name=None, search_country=None):
    """
    SELECT
        tennisplayer.*,
    FROM tennisplayer
    WHERE
        full_name ILIKE "%search_name%"
        AND country ILIKE "%search_county%"
    ORDER BY
        ranking ASC
    ;
    """

    if search_name is None and search_country is None:
        return ""

    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(
            Q(full_name__icontains = search_name) &
            Q(country__icontains = search_country)
        )

    elif search_name is not None:
        players = TennisPlayer.objects.filter(
            full_name__icontains = search_name
        )

    else:
        players = TennisPlayer.objects.filter(
            country__icontains = search_country
        )

    players = players.order_by(
        'ranking'
    )


    if not players.exists():
        return ""

    return "\n".join(
        f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}" for p in players
    )

def get_top_tennis_player():

    """
    SELECT
        tennisplayer.*,
        COUNT(match.id) AS wins_count
    FROM tennisplayer
    LEFT JOIN match
        ON tennisplayer.id = match.winner_id
    GROUP BY
        tennisplayer.id
    ORDER BY
        wins_count DESC,
        tennisplayer.full_name ASC
    LIMIT 1;
    """

    player = TennisPlayer.objects.annotate(
        wins_count = Count('won_matches')
    ).order_by(
        '-wins_count',
        'full_name'
    ).first()

    if not player:
        return ""

    return (
        f"Top Tennis Player: {player.full_name} with {player.wins_count} wins."
    )

def get_tennis_player_by_matches_count():

    """
    SELECT
        tennisplayer.*,
        COUNT(match.id) AS wins_count
    FROM tennisplayer
    LEFT JOIN match
        ON tennisplayer.id = match.winner_id
    GROUP BY
        tennisplayer.id
    ORDER BY
        wins_count DESC,
        tennisplayer.full_name ASC
    LIMIT 1;
    """

    player = TennisPlayer.objects.annotate(
        matches_count = Count('matches')
    ).order_by(
        '-matches_count',
        'ranking',
    ).first()

    if not player or player.matches_count == 0:
        return ""

    return (
        f"Tennis Player: {player.full_name} with {player.matches_count} matches played."
    )


def get_tournaments_by_surface_type(surface=None):

    """
    SELECT
        tournament.*,
        COUNT(match.id) AS num_matches
    FROM tournament
    LEFT JOIN match
        ON tournament.id = match.tournament_id
    WHERE
        surface_type ILIKE '%surface%'
    GROUP BY
        tournament.id
    ORDER BY
        start_date DESC;
    """

    if not surface:
        return ""

    tournaments = Tournament.objects.annotate(
        num_matches = Count('matches')
    ).filter(
        surface_type__icontains = surface
    ).order_by(
        '-start_date'
    )

    if not tournaments.exists():
        return ""

    return "\n".join(
        f"Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}" for t in tournaments
    )

def get_latest_match_info():
    """
    SELECT
        match.*,
        tournament.name AS tournament_name,
        winner.full_name AS winner_name
    FROM match
    LEFT JOIN tournament
        ON match.tournament_id = tournament.id
    LEFT JOIN tennisplayer AS winner
        ON match.winner_id = winner.id
    ORDER BY
        match.date_played DESC,
        match.id DESC
    LIMIT 1;
    """

    match = Match.objects.select_related(
        'tournament',
        'winner',
    ).prefetch_related(
        'players',
    ).order_by(
        '-date_played',
        '-id',
    ).first()

    if not match:
        return ""

    players = match.players.all().order_by('full_name')

    player_names = " vs ".join(p.full_name for p in players)

    winner = match.winner.full_name if match.winner else "TBA"

    tournament_name = match.tournament.name

    return (f"Latest match played on: {match.date_played}, "
            f"tournament: {tournament_name}, score: {match.score}, "
            f"players: {player_names}, "
            f"winner: {winner}, summary: {match.summary}")

def get_matches_by_tournament(tournament_name=None):
    """
    SELECT
        match.*,
        winner.full_name AS winner_name
    FROM match
    JOIN tournament
        ON match.tournament_id = tournament.id
    LEFT JOIN tennisplayer AS winner
        ON match.winner_id = winner.id
    WHERE
        tournament.name = 'tournament_name'
    ORDER BY
        match.date_played DESC;
    """

    if tournament_name is None:
        return "No matches found."

    matches = Match.objects.select_related(
        'tournament',
        'winner',
    ).filter(
        tournament__name = tournament_name
    ).order_by(
        '-date_played'
    )

    if not matches.exists():
        return "No matches found."

    return "\n".join(
        f"Match played on: {m.date_played}, "
        f"score: {m.score}, "
        f"winner: {m.winner.full_name if m.winner else 'TBA'}" for m in matches
    )