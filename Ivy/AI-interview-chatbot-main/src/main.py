from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from typing import List, Optional
import json

from .database import SessionLocal, engine
from . import models, schemas
from .config import settings
from .auth import get_current_user, create_access_token
from .websocket_manager import ConnectionManager

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ivy - Interview Virtual Assistant API",
    description="Backend API for the Ivy interview platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
manager = ConnectionManager()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication endpoints
@app.post("/auth/token", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = await authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_new_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Interview endpoints
@app.post("/interviews/", response_model=schemas.Interview)
async def create_interview(
    interview: schemas.InterviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return await create_new_interview(db=db, interview=interview, user_id=current_user.id)

@app.get("/interviews/", response_model=List[schemas.Interview])
async def list_interviews(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    interviews = await get_user_interviews(db, user_id=current_user.id, skip=skip, limit=limit)
    return interviews

@app.get("/interviews/{interview_id}", response_model=schemas.Interview)
async def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    interview = await get_interview_by_id(db, interview_id=interview_id)
    if interview is None or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview

# Analytics endpoints
@app.get("/analytics/overview", response_model=schemas.AnalyticsOverview)
async def get_analytics_overview(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return await generate_analytics_overview(db, user_id=current_user.id)

@app.get("/analytics/trends", response_model=schemas.AnalyticsTrends)
async def get_analytics_trends(
    timeframe: str = "30d",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return await generate_analytics_trends(db, user_id=current_user.id, timeframe=timeframe)

# WebSocket endpoint for real-time features
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Process the received data
            message = json.loads(data)
            # Handle different message types
            if message["type"] == "interview_update":
                # Broadcast interview updates to all connected clients
                await manager.broadcast(json.dumps({
                    "type": "interview_update",
                    "data": message["data"]
                }))
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        await manager.broadcast(f"Client #{client_id} left the interview")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()} 