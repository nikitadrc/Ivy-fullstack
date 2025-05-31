import pytest
from fastapi import status

def test_create_user(client):
    user_data = {
        "email": "newuser@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_login(client, test_user):
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/token", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    login_data = {
        "username": "wrong@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/token", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user(client, test_user):
    # First login to get the token
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    login_response = client.post("/api/token", data=login_data)
    token = login_response.json()["access_token"]
    
    # Use token to get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com" 