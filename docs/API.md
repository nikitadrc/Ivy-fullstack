# AI Interview Chatbot API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication
All API endpoints require JWT authentication except for `/auth/login` and `/auth/register`.
Include the JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password",
    "name": "John Doe",
    "role": "candidate"  // or "interviewer"
}

Response: 201 Created
{
    "id": "user_id",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "candidate"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "secure_password"
}

Response: 200 OK
{
    "access_token": "jwt_token",
    "token_type": "bearer"
}
```

### Interviews

#### Schedule Interview
```http
POST /interviews
Content-Type: application/json

{
    "candidate_id": "candidate_user_id",
    "interviewer_id": "interviewer_user_id",
    "scheduled_time": "2024-03-20T14:00:00Z",
    "duration_minutes": 60,
    "position": "Software Engineer"
}

Response: 201 Created
{
    "id": "interview_id",
    "status": "scheduled",
    "meeting_link": "https://meet.google.com/..."
}
```

#### Get Interview Details
```http
GET /interviews/{interview_id}

Response: 200 OK
{
    "id": "interview_id",
    "candidate": {
        "id": "user_id",
        "name": "John Doe",
        "email": "john@example.com"
    },
    "interviewer": {
        "id": "user_id",
        "name": "Jane Smith",
        "email": "jane@example.com"
    },
    "scheduled_time": "2024-03-20T14:00:00Z",
    "duration_minutes": 60,
    "status": "scheduled",
    "meeting_link": "https://meet.google.com/...",
    "materials_url": "https://storage.example.com/..."
}
```

#### List Interviews
```http
GET /interviews?status=scheduled&role=candidate

Response: 200 OK
{
    "items": [
        {
            "id": "interview_id",
            "scheduled_time": "2024-03-20T14:00:00Z",
            "status": "scheduled",
            // ... other interview details
        }
    ],
    "total": 10,
    "page": 1,
    "per_page": 20
}
```

#### Update Interview Status
```http
PATCH /interviews/{interview_id}
Content-Type: application/json

{
    "status": "completed",
    "feedback": "Candidate demonstrated strong technical skills..."
}

Response: 200 OK
{
    "id": "interview_id",
    "status": "completed",
    "feedback": "Candidate demonstrated strong technical skills..."
}
```

### Calendar

#### Get Available Slots
```http
GET /calendar/available-slots?start_date=2024-03-20&end_date=2024-03-21

Response: 200 OK
{
    "slots": [
        "2024-03-20T09:00:00Z",
        "2024-03-20T10:00:00Z",
        // ... more available slots
    ]
}
```

### Files

#### Upload Interview Materials
```http
POST /files/upload
Content-Type: multipart/form-data

file: <file_data>
interview_id: "interview_id"

Response: 201 Created
{
    "file_url": "https://storage.example.com/...",
    "file_type": "application/pdf",
    "file_size": 1024
}
```

#### List Interview Materials
```http
GET /files/interview/{interview_id}

Response: 200 OK
{
    "files": [
        {
            "url": "https://storage.example.com/...",
            "name": "resume.pdf",
            "uploaded_at": "2024-03-20T12:00:00Z"
        }
    ]
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "validation_error",
    "message": "Invalid input data",
    "details": {
        "field": ["error message"]
    }
}
```

### 401 Unauthorized
```json
{
    "error": "unauthorized",
    "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
    "error": "forbidden",
    "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
    "error": "not_found",
    "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "internal_server_error",
    "message": "An unexpected error occurred"
}
``` 