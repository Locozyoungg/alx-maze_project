# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

user_song_association = Table(
    'user_song_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('song_id', Integer, ForeignKey('songs.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    songs = relationship("Song", secondary=user_song_association, back_populates="users")

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String)
    users = relationship("User", secondary=user_song_association, back_populates="songs")

