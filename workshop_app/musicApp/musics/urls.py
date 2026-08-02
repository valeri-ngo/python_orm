from django.urls import path, include
from musics.views import create_album, create_song, delete_album, details_album, edit_album, index


urlpatterns = [
    path('', index, name='index'),
    path('album/', include([
        path('create/', create_album, name='create-album'),
        path('<int:pk>/', include([
            path('edit/', edit_album, name='edit-album'),
            path('delete/', delete_album, name='delete-album'),
            path('details/', details_album, name='details-album')
        ])),
    ])),
    path('song/', include([
        path('create/', create_song, name='create-song')
    ])),
]