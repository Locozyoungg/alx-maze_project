from fastapi.testclient import TestClient
from app.main import app
from app import schemas, models
from app.database import SessionLocal, engine
import pytest
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_client():
    models.Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user(test_client):
    response = test_client.post("/users/", json={"username": "testuser", "email": "testuser@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_login_for_access_token(test_client):
    response = test_client.post("/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_read_users_me(test_client):
    login_response = test_client.post("/token", data={"username": "testuser", "password": "password"})
    token = login_response.json()["access_token"]
    response = test_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_create_song_for_user(test_client, db_session):
    user = db_session.query(models.User).filter(models.User.username == "testuser").first()
    response = test_client.post(f"/users/{user.id}/songs/", json={"title": "Test Song", "artist": "Test Artist"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Song"

def test_get_recommendations(test_client, db_session):
    user = db_session.query(models.User).filter(models.User.username == "testuser").first()
    response = test_client.get(f"/recommendations/{user.id}/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

