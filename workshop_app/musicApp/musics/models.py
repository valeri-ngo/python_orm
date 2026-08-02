from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from musicApp import settings


# Create your models here.

class Album(settings.BaseModel):
    __tablename__ = 'albums'

    id = Column(
        Integer,
        primary_key=True,
    )

    album_name = Column(
        String(30),
        nullable=False,
    )

    image_url = Column(
        String,
        nullable=False,
    )

    price = Column(
        Float,
        nullable=False,
    )

    songs = relationship(
        'Song',
        back_populates = 'album',
        cascade='all, delete-orphan',
    )

    def __str__(self):
        return self.album_name
    


class Song(settings.BaseModel):
    __tablename__ = 'songs'

    id = Column(
        Integer,
        primary_key=True,
    )

    song_name = Column(
        String
    )

    album_id = Column(
        Integer,
        ForeignKey('albums.id'),
        nullable=False,
    )

    album = relationship(
        'Album',
        back_populates='songs',
    )

    def __str__(self):
        return self.song_name
    