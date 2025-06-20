import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Set up env vars for config before importing app
os.environ.setdefault("DB_TEST_URL", settings.DB_TEST_URL)
os.environ.setdefault("JWT_ACCESS_SECRET_KEY", settings.JWT_ACCESS_SECRET_KEY)
os.environ.setdefault("JWT_REFRESH_SECRET_KEY", settings.JWT_ACCESS_SECRET_KEY)

if os.path.exists("./test.db"):
    os.remove("./test.db")

from app.db.base import Base
from app.main import app
from app.api.deps import get_db
from app.db.models.board import Board

# Use SQLite database for testing
TEST_ENGINE = create_engine(
    os.environ["DB_TEST_URL"], connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)

# Create tables
Base.metadata.create_all(bind=TEST_ENGINE)

# Dependency override

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def create_board(db, name="general"):
    board = Board(name=name, description="test board")
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


def signup_and_login(username="alice"):
    signup_data = {
        "username": username,
        "lastname": "Kim",
        "firstname": "Alice",
        "email": f"{username}@example.com",
        "password": "secret",
    }
    r = client.post("/api/v1/auth/signup", json=signup_data)
    assert r.status_code == 201
    login_data = {"username": username, "password": "secret"}
    r = client.post("/api/v1/auth/login", json=login_data)
    assert r.status_code == 200
    return r.json()["access_token"]


def test_signup_login_me():
    token = signup_and_login()
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/api/v1/users/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "alice"


def test_create_post():
    token = signup_and_login("bob")
    headers = {"Authorization": f"Bearer {token}"}
    # create board directly in DB
    with TestingSessionLocal() as db:
        board = create_board(db)
        board_id = board.id
    post_data = {"title": "Hello", "content": "World", "board_id": board_id}
    r = client.post(f"/api/v1/posts/boards/{board_id}/posts", json=post_data, headers=headers)
    assert r.status_code == 201
    post_id = r.json()["id"]
    r = client.get(f"/api/v1/posts/boards/{board_id}/posts/{post_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Hello"


def test_get_all_boards():
    token = signup_and_login("board_user")
    headers = {"Authorization": f"Bearer {token}"}

    with TestingSessionLocal() as db:
        board = create_board(db, name="general2")
        board_id = board.id

    post_data = {"title": "hello", "content": "world", "board_id": board_id}
    r = client.post(
        f"/api/v1/posts/boards/{board_id}/posts",
        json=post_data,
        headers=headers,
    )
    assert r.status_code == 201

    r = client.get("/api/v1/boards/all_boards")
    assert r.status_code == 200
    data = r.json()
    board_data = next(b for b in data if b["id"] == board_id)
    assert board_data["posts"] == 1
    assert "created_at" in board_data


def test_post_with_file():
    token = signup_and_login("file_user")
    headers = {"Authorization": f"Bearer {token}"}

    with TestingSessionLocal() as db:
        board = create_board(db, name="fileboard")
        board_id = board.id

    post_data = {"title": "file", "content": "check", "board_id": board_id}
    r = client.post(
        f"/api/v1/posts/boards/{board_id}/posts",
        json=post_data,
        headers=headers,
    )
    assert r.status_code == 201
    post_id = r.json()["id"]

    files = {"file": ("hello.txt", b"hello", "text/plain")}
    r = client.post(
        f"/api/v1/posts/{post_id}/files",
        files=files,
        headers=headers,
    )
    assert r.status_code == 201
    file_id = r.json()["id"]
    assert r.json()["url"] == f"/api/v1/files/{file_id}/download"

    r = client.get(f"/api/v1/posts/boards/{board_id}/posts/{post_id}")
    assert r.status_code == 200
    data = r.json()
    assert len(data["files"]) == 1
    assert data["files"][0]["id"] == file_id
    assert data["files"][0]["url"] == f"/api/v1/files/{file_id}/download"
