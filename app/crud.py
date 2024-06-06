# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def get_songs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Song).offset(skip).limit(limit).all()

def create_user_song(db: Session, song: schemas.SongCreate, user_id: int):
    db_song = models.Song(**song.dict())
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.songs.append(db_song)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

