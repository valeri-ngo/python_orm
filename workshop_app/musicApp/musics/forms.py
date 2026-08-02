from typing import List

from django import forms
from musicApp.settings import session
from musicApp.utils import handle_session

from musics.models import Album


class DisabledFieldsMixin(forms.Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['disabled'] = True


class AlbumBaseForm(forms.Form):
    album_name = forms.CharField(
        label='Album name:',
        max_length=30,
        required=True,
    )

    image_url = forms.URLField(
        label='Image URL:',
        required=True,
    )

    price = forms.DecimalField(
        label='Price:',
        min_value=0.0,
        required=True,
    )


class AlbumCreateForm(AlbumBaseForm):
    pass


class AlbumEditForm(AlbumBaseForm):
    pass


class AlbumDeleteForm(DisabledFieldsMixin, AlbumBaseForm):
    pass


class SongBaseForm(forms.Form):
    song_name = forms.CharField(
        max_length=200,
        required=True,
    )

    album = forms.ChoiceField(
        label='Album:',
        choices=[],
    )


    @handle_session(session)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        albums: list[Album] = session.query(Album).all()

        field = self.fields['album']
        assert isinstance(field, forms.ChoiceField)

        field.choices = [
            (album.id, album.album_name)
            for album in albums
        ]


class SongCreateForm(SongBaseForm):
    pass