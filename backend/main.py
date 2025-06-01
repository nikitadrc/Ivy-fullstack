from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_db
from models import User, Message, Feedback, ProgressTrack
from schemas import (
    UserCreate, User as UserSchema,
    MessageCreate, Message as MessageSchema,
    ChatResponse, FeedbackCreate, FeedbackResponse,
    ProgressResponse, StudyStreak, Token
)
from security import (
    get_current_user, create_access_token,
    authenticate_user, get_password_hash
)
from services.rag_service import RAGService
from services.progress_service import ProgressService

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
rag_service = RAGService()

# WebSocket connections store
active_connections: dict = {}

@app.post("/api/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/users/", response_model=UserSchema)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        selected_role=user.selected_role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/users/me", response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@app.post("/api/chat/{user_id}", response_model=ChatResponse)
async def send_message(
    user_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Save user message
    db_message = Message(
        user_id=user_id,
        content=message.content,
        role="user",
        question_type=message.question_type
    )
    db.add(db_message)
    db.commit()

    # Generate response
    response = rag_service.get_response(
        message.content,
        current_user.selected_role,
        message.question_type
    )

    # Save assistant message
    assistant_message = Message(
        user_id=user_id,
        content=response["answer"],
        role="assistant",
        question_type=message.question_type
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)

    # Update progress
    progress_service = ProgressService(db)
    progress_service.update_progress(
        user_id=user_id,
        topic=message.question_type
    )

    return {
        "id": assistant_message.id,
        "answer": response["answer"],
        "context_used": response["context_used"],
        "confidence_score": response["confidence_score"],
        "suggested_topics": response["suggested_topics"]
    }

@app.get("/api/chat/{user_id}/history", response_model=List[MessageSchema])
async def get_chat_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    messages = db.query(Message).filter(
        Message.user_id == user_id
    ).order_by(Message.timestamp.desc()).all()
    return messages

@app.post("/api/chat/{message_id}/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    message_id: int,
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_feedback = Feedback(
        message_id=message_id,
        rating=feedback.rating,
        was_helpful=feedback.was_helpful,
        comment=feedback.comment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/api/users/{user_id}/progress", response_model=ProgressResponse)
async def get_user_progress(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    progress_service = ProgressService(db)
    return progress_service.get_user_progress(user_id)

@app.get("/api/users/{user_id}/streak", response_model=StudyStreak)
async def get_study_streak(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    progress_service = ProgressService(db)
    return progress_service.get_study_streak(user_id)

@app.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_json()
            # Handle different types of WebSocket messages
            if data["type"] == "typing":
                # Broadcast typing status to other users
                for uid, conn in active_connections.items():
                    if uid != user_id:
                        await conn.send_json({
                            "type": "typing",
                            "user_id": user_id,
                            "is_typing": data["is_typing"]
                        })
    except WebSocketDisconnect:
        if user_id in active_connections:
            del active_connections[user_id] 