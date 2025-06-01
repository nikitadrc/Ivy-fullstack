from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class RoleType(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    DATA_SCIENTIST = "data_scientist"
    DEVOPS = "devops"
    AI_ML = "ai_ml"
    QA = "qa"

class QuestionType(str, Enum):
    TECHNICAL = "technical"
    CODING = "coding"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"
    RESUME = "resume"

class UserBase(BaseModel):
    email: EmailStr
    name: str
    selected_role: RoleType

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    content: str
    question_type: QuestionType

class MessageCreate(MessageBase):
    user_id: int
    role: str

class Message(MessageBase):
    id: int
    timestamp: datetime
    user_id: int

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    id: int
    answer: str
    context_used: List[str]
    confidence_score: float
    suggested_topics: List[str]

class FeedbackCreate(BaseModel):
    rating: int
    was_helpful: bool
    comment: Optional[str] = None

class FeedbackResponse(FeedbackCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProgressResponse(BaseModel):
    overall_progress: float
    topic_progress: dict[str, float]
    recommendations: List[str]

class StudyStreak(BaseModel):
    current_streak: int
    longest_streak: int
    last_study_date: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 