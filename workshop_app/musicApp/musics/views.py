from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from musicApp.settings import session
from musicApp.utils import handle_session

from musics.models import Album, Song

from .forms import AlbumCreateForm, AlbumDeleteForm, AlbumEditForm, SongCreateForm

# Create your views here.

@handle_session(session)
def index(request) -> HttpResponse:
    context: dict[str, list[Album]] = {
        'albums': session.query(Album).all()
    }

    return render(request, 'common/index.html', context)


@handle_session(session)
def create_album(request) -> HttpResponse:
    form = AlbumCreateForm(request.POST or None)

    context: dict[str, AlbumCreateForm] = {
        'form': AlbumCreateForm()
    }

    if request.method == 'POST'and form.is_valid():
            new_album = Album(
                album_name = form.cleaned_data['album_name'],
                image_url = form.cleaned_data['image_url'],
                price = form.cleaned_data['price'],
            )

            session.add(new_album)

            return redirect(to='index')

    return render(request, 'albums/create-album.html', context)


@handle_session(session)
def edit_album(request, pk: int) -> HttpResponse:
    album: Album | None = session.query(Album).filter_by(id=pk).first()


    if album is None:
        return redirect("index")

    form = AlbumEditForm(
         request.POST or None,
         initial={
              'album_name': album.album_name,
              'image_url': album.image_url,
              'price': album.price,
         }
    )

    if request.method == 'POST' and form.is_valid():
         album.album_name = form.cleaned_data['album_name']
         album.image_url = form.cleaned_data['image_url']
         album.price = form.cleaned_data['price']

         return redirect('index')

    context = {
         'form': form
    }

    return render(request, 'albums/edit-album.html', context)


@handle_session(session)
def delete_album(request, pk: int) -> HttpResponse:
    album: Album | None = session.query(Album).filter_by(id=pk).first()

    if album is None:
        return redirect("index")

    form = AlbumDeleteForm(
        initial={
            'album_name': album.album_name,
            'image_url': album.image_url,
            'price': album.price,
        }
    )

    if request.method == 'POST':
        session.delete(album)
        return redirect('index')

    context: dict[str, AlbumDeleteForm] = {
        'form': form
    }

    return render(request, 'albums/delete-album.html', context)


@handle_session(session)
def details_album(request, pk: int) -> HttpResponse:
    context: dict[str, Album | None] = {
        'album': session.query(Album).filter_by(id=pk).first()
    }

    return render(request, 'albums/album-details.html', context)


@handle_session(session)
def create_song(request) -> HttpResponse:
    form = SongCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        song = Song(
            song_name = form.cleaned_data['song_name'],
            album_id = form.cleaned_data['album']
        )

        session.add(song)

        return redirect('index')

    context = {
        'form': form
    }

    return render(request, 'songs/create-song.html', context)