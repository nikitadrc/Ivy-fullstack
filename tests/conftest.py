import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.services.calendar_service import CalendarService
from src.services.email_service import EmailService
from src.services.storage_service import StorageService
import os
import tempfile
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from src.database import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_interview_bot"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(client, db_session):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def mock_calendar_credentials():
    """Mock Google Calendar credentials"""
    return {
        "token": "mock_token",
        "refresh_token": "mock_refresh_token",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "mock_client_id",
        "client_secret": "mock_client_secret",
        "scopes": ["https://www.googleapis.com/auth/calendar"]
    }

@pytest.fixture
def mock_calendar_service(mocker):
    """Mock calendar service"""
    service = CalendarService()
    mocker.patch.object(service, '_initialize_service')
    return service

@pytest.fixture
def mock_email_service(mocker):
    """Mock email service"""
    service = EmailService(api_key="mock_api_key")
    mocker.patch.object(service.client, 'send', return_value=mocker.Mock(to_dict=lambda: {"status": "success"}))
    return service

@pytest.fixture
def mock_storage_service(mocker):
    """Mock storage service"""
    service = StorageService(
        aws_access_key_id="mock_key",
        aws_secret_access_key="mock_secret",
        region_name="us-east-1",
        bucket_name="test-bucket"
    )
    mocker.patch.object(service, 's3_client')
    return service

@pytest.fixture
def temp_file():
    """Create a temporary file for testing"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"Test content")
        tmp.flush()
        yield tmp.name
    os.unlink(tmp.name)

@pytest.fixture
def future_datetime():
    """Get a future datetime for testing"""
    return datetime.now() + timedelta(days=1)

@pytest.fixture
def sample_interview_data():
    """Sample interview data for testing"""
    return {
        "candidate_name": "John Doe",
        "candidate_email": "john@example.com",
        "interviewer_email": "interviewer@example.com",
        "position": "Software Engineer",
        "scheduled_time": datetime.now() + timedelta(days=1),
        "duration_minutes": 60
    } 