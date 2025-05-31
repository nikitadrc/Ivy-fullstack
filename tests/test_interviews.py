import pytest
from fastapi import status
from datetime import datetime, timedelta

@pytest.fixture
def auth_headers(client, test_user):
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_interview(client, auth_headers):
    interview_data = {
        "title": "Test Interview",
        "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat()
    }
    response = client.post("/api/interviews/", json=interview_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == interview_data["title"]
    assert "id" in data

def test_get_interview(client, auth_headers):
    # First create an interview
    interview_data = {
        "title": "Test Interview",
        "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat()
    }
    create_response = client.post("/api/interviews/", json=interview_data, headers=auth_headers)
    interview_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/interviews/{interview_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == interview_data["title"]
    assert data["id"] == interview_id

def test_list_interviews(client, auth_headers):
    # Create multiple interviews
    for i in range(3):
        interview_data = {
            "title": f"Test Interview {i}",
            "scheduled_at": (datetime.utcnow() + timedelta(days=i+1)).isoformat()
        }
        client.post("/api/interviews/", json=interview_data, headers=auth_headers)
    
    response = client.get("/api/interviews/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 3
    assert all(isinstance(interview["id"], int) for interview in data)

def test_update_interview(client, auth_headers):
    # First create an interview
    interview_data = {
        "title": "Original Title",
        "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat()
    }
    create_response = client.post("/api/interviews/", json=interview_data, headers=auth_headers)
    interview_id = create_response.json()["id"]
    
    # Update it
    update_data = {
        "title": "Updated Title",
        "scheduled_at": (datetime.utcnow() + timedelta(days=2)).isoformat()
    }
    response = client.put(f"/api/interviews/{interview_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]

def test_delete_interview(client, auth_headers):
    # First create an interview
    interview_data = {
        "title": "To Be Deleted",
        "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat()
    }
    create_response = client.post("/api/interviews/", json=interview_data, headers=auth_headers)
    interview_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/interviews/{interview_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's gone
    get_response = client.get(f"/api/interviews/{interview_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND 