import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app
from ..models import User
from ..security import get_password_hash

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user = User(
        email="test@example.com",
        name="Test User",
        hashed_password=get_password_hash("testpassword"),
        selected_role="frontend"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def test_create_user():
    response = client.post(
        "/api/users/",
        json={
            "email": "new@example.com",
            "name": "New User",
            "password": "newpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data

def test_get_chat_history(test_user):
    response = client.get(f"/api/chat/{test_user.id}/history")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data

def test_send_message(test_user):
    response = client.post(
        f"/api/chat/{test_user.id}",
        json={
            "question_type": "technical",
            "message": "What is React?"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "context_used" in data
    assert "suggested_topics" in data

def test_submit_feedback(test_user):
    # First send a message to get a message_id
    message_response = client.post(
        f"/api/chat/{test_user.id}",
        json={
            "question_type": "technical",
            "message": "What is Python?"
        }
    )
    message_id = message_response.json()["id"]

    # Submit feedback
    response = client.post(
        f"/api/chat/{message_id}/feedback",
        json={
            "rating": 5,
            "was_helpful": True,
            "comment": "Great explanation!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["was_helpful"] == True

def test_get_user_progress(test_user):
    response = client.get(f"/api/users/{test_user.id}/progress")
    assert response.status_code == 200
    data = response.json()
    assert "overall_progress" in data
    assert "topic_progress" in data
    assert "recommendations" in data

def test_get_study_streak(test_user):
    response = client.get(f"/api/users/{test_user.id}/streak")
    assert response.status_code == 200
    data = response.json()
    assert "current_streak" in data
    assert "longest_streak" in data
    assert "last_study_date" in data 