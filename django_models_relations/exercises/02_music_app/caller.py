import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Artist, Song

# Create queries within functions

def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name = artist_name)
    song = Song.objects.get(title = song_title)

    artist.songs.add(song)

def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name = artist_name)

    return artist.songs.all().order_by('-id')

def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name = artist_name)
    song = Song.objects.get(title = song_title)

    artist.songs.remove(song)

# Print