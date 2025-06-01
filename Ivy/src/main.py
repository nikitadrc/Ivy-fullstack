from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import jwt
from jwt.exceptions import PyJWTError
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi import UploadFile, File, Query, WebSocket

from .database import get_db, engine
from .models import Base, User, Interview
from .schemas import (
    UserCreate, UserResponse, InterviewCreate, InterviewResponse,
    Token, TokenData, InterviewUpdate, File
)
from .services.calendar_service import CalendarService
from .services.email_service import EmailService
from .services.storage_service import StorageService
from .services.auth import create_access_token, get_current_user
from .services.rag_service import RAGService
from .services.progress_service import ProgressService

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Interview Chatbot API",
    description="""
    The AI Interview Chatbot API provides endpoints for managing interview sessions,
    user authentication, and interview feedback. This API allows users to:
    
    * Create and manage user accounts
    * Schedule and manage interview sessions
    * Record and analyze interview responses
    * Get AI-powered feedback and suggestions
    * Manage file uploads and attachments
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Initialize services
calendar_service = CalendarService()
email_service = EmailService()
storage_service = StorageService()
rag_service = RAGService()
progress_service = ProgressService()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Authentication endpoints
@app.post("/api/token", response_model=Token, tags=["authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Get an access token for authentication.
    
    - **username**: Email address of the user
    - **password**: User's password
    
    Returns an access token that can be used for authenticated endpoints.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    
    - **email**: Valid email address
    - **password**: Strong password (min 8 characters)
    
    Returns the created user information (excluding password).
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Interview endpoints
@app.post("/api/interviews/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED, tags=["interviews"])
def create_interview(
    interview: InterviewCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new interview session.
    
    - **title**: Title of the interview
    - **scheduled_at**: When the interview is scheduled (ISO format)
    
    Returns the created interview information.
    """
    # Verify permissions
    if current_user.role not in ["admin", "interviewer"]:
        raise HTTPException(status_code=403, detail="Not authorized to create interviews")
    
    # Create interview
    db_interview = Interview(**interview.dict())
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    # Schedule in calendar
    calendar_event = calendar_service.create_interview_event(
        interviewer_email=db_interview.interviewer.email,
        candidate_email=db_interview.candidate.email,
        start_time=db_interview.scheduled_time,
        duration_minutes=db_interview.duration_minutes
    )

    # Update interview with calendar event details
    db_interview.calendar_event_id = calendar_event['id']
    db_interview.meeting_link = calendar_event.get('hangoutLink')
    db.commit()

    # Send email notifications
    email_service.send_interview_scheduled(
        to_email=db_interview.candidate.email,
        name=db_interview.candidate.name,
        date=db_interview.scheduled_time.strftime('%Y-%m-%d'),
        time=db_interview.scheduled_time.strftime('%H:%M'),
        meeting_link=db_interview.meeting_link
    )

    return db_interview

@app.get("/api/interviews/", response_model=List[InterviewResponse], tags=["interviews"])
def list_interviews(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List all interviews for the current user.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    
    Returns a list of interviews.
    """
    query = db.query(Interview)
    
    # Filter by user role
    if current_user.role == "candidate":
        query = query.filter(Interview.candidate_id == current_user.id)
    elif current_user.role == "interviewer":
        query = query.filter(Interview.interviewer_id == current_user.id)
    
    return query.offset(skip).limit(limit).all()

@app.get("/api/interviews/{interview_id}", response_model=InterviewResponse, tags=["interviews"])
def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific interview.
    
    - **interview_id**: ID of the interview to retrieve
    
    Returns the interview information if found and owned by the current user.
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Check permissions
    if (current_user.id != interview.candidate_id and 
        current_user.id != interview.interviewer_id and
        current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to view this interview")
    
    return interview

@app.patch("/interviews/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: int,
    interview_update: InterviewUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not db_interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Check permissions
    if (current_user.id != db_interview.interviewer_id and
        current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to update this interview")
    
    # Update interview
    for field, value in interview_update.dict(exclude_unset=True).items():
        setattr(db_interview, field, value)
    
    db.commit()
    db.refresh(db_interview)

    # Send feedback email if interview is completed
    if interview_update.status == "completed" and interview_update.feedback:
        email_service.send_interview_feedback(
            to_email=db_interview.candidate.email,
            name=db_interview.candidate.name,
            feedback=interview_update.feedback
        )

    return db_interview

# File upload endpoints
@app.post("/api/files/", response_model=File, tags=["files"])
async def upload_file(
    interview_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload a file for an interview.
    
    - **interview_id**: ID of the interview to attach the file to
    - **file**: The file to upload
    
    Returns the file metadata including the S3 storage key.
    """
    # ... existing implementation ...

# WebSocket endpoint for real-time chat
@app.websocket("/ws/interview/{interview_id}")
async def interview_websocket(
    websocket: WebSocket,
    interview_id: int,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time interview chat.
    
    - **interview_id**: ID of the interview session
    - **token**: Valid JWT access token
    
    Establishes a WebSocket connection for real-time communication during the interview.
    """
    # ... existing implementation ...

@app.post("/users/{user_id}/role", response_model=User)
def set_user_role(
    user_id: int,
    role: RoleType,
    db: Session = Depends(get_db)
):
    """Set or update the user's selected role"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.selected_role = role
    db.commit()
    db.refresh(user)
    return user

@app.post("/chat/{user_id}", response_model=ChatResponse)
async def process_chat(
    user_id: int,
    chat_request: ChatSessionCreate,
    db: Session = Depends(get_db)
):
    """Process a chat message and return response"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.selected_role:
        raise HTTPException(
            status_code=400,
            detail="Please select a role before starting chat"
        )
    
    # Create new chat session
    chat_session = ChatSession(
        user_id=user_id,
        question_type=chat_request.question_type,
        chat_history=chat_request.chat_history
    )
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    
    # Process the question
    response = rag_service.process_question(
        question=chat_request.chat_history[-1]["content"],
        role=user.selected_role,
        question_type=chat_request.question_type,
        chat_history=chat_request.chat_history[:-1]
    )
    
    # Update progress
    progress_service = ProgressService(db)
    progress_service.update_progress(
        user_id=user_id,
        topic=chat_request.question_type.value
    )
    
    return response

@app.get("/users/{user_id}/progress", response_model=Dict[str, float])
def get_progress(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user's progress across all topics"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    progress_service = ProgressService(db)
    return progress_service.get_user_progress(user_id)

@app.get("/users/{user_id}/recommendations", response_model=List[Dict[str, Any]])
def get_recommendations(
    user_id: int,
    limit: int = 3,
    db: Session = Depends(get_db)
):
    """Get recommended topics for the user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    progress_service = ProgressService(db)
    return progress_service.get_recommended_topics(user_id, limit)

@app.get("/users/{user_id}/streak", response_model=int)
def get_study_streak(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user's current study streak"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    progress_service = ProgressService(db)
    return progress_service.get_study_streak(user_id)

@app.post("/chat/{chat_session_id}/feedback", response_model=Feedback)
def submit_feedback(
    chat_session_id: int,
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """Submit feedback for a chat session"""
    chat_session = db.query(ChatSession).filter(
        ChatSession.id == chat_session_id
    ).first()
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    new_feedback = Feedback(
        chat_session_id=chat_session_id,
        rating=feedback.rating,
        was_helpful=feedback.was_helpful,
        comment=feedback.comment
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 