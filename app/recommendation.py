# app/recommendation.py
from typing import List
from sqlalchemy.orm import Session
from . import models

def recommend_songs(user_id: int, db: Session) -> List[models.Song]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return []
    user_song_ids = [song.id for song in user.songs]
    recommended_songs = db.query(models.Song).filter(models.Song.id.notin_(user_song_ids)).all()
    return recommended_songs

