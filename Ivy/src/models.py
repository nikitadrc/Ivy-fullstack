from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class RoleType(enum.Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    FULLSTACK = "fullstack"
    DATA_SCIENTIST = "data_scientist"
    DEVOPS = "devops"
    AI_ML = "ai_ml"
    QA = "qa"

class QuestionType(enum.Enum):
    TECHNICAL = "technical"
    CODING = "coding"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"
    RESUME = "resume"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    selected_role = Column(Enum(RoleType))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    interviews_as_candidate = relationship(
        "Interview",
        back_populates="candidate",
        foreign_keys="Interview.candidate_id"
    )
    interviews_as_interviewer = relationship(
        "Interview",
        back_populates="interviewer",
        foreign_keys="Interview.interviewer_id"
    )
    chat_sessions = relationship("ChatSession", back_populates="user")
    progress_tracks = relationship("ProgressTrack", back_populates="user")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"))
    interviewer_id = Column(Integer, ForeignKey("users.id"))
    position = Column(String)
    scheduled_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer, default=60)
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, cancelled
    feedback = Column(Text)
    calendar_event_id = Column(String)
    meeting_link = Column(String)
    materials_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    candidate = relationship(
        "User",
        back_populates="interviews_as_candidate",
        foreign_keys=[candidate_id]
    )
    interviewer = relationship(
        "User",
        back_populates="interviews_as_interviewer",
        foreign_keys=[interviewer_id]
    )
    questions = relationship("InterviewQuestion", back_populates="interview")
    responses = relationship("InterviewResponse", back_populates="interview")

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_text = Column(Text)
    question_type = Column(Enum(QuestionType))
    order = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    interview = relationship("Interview", back_populates="questions")
    responses = relationship("InterviewResponse", back_populates="question")

class InterviewResponse(Base):
    __tablename__ = "interview_responses"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_id = Column(Integer, ForeignKey("interview_questions.id"))
    response_text = Column(Text)
    score = Column(Integer)  # 1-5 scale
    feedback = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    interview = relationship("Interview", back_populates="responses")
    question = relationship("InterviewQuestion", back_populates="responses")

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    upload_time = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    interview_id = Column(Integer, ForeignKey("interviews.id"))

    # Relationships
    user = relationship("User")
    interview = relationship("Interview")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_type = Column(Enum(QuestionType))
    chat_history = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="chat_sessions")
    feedback = relationship("Feedback", back_populates="chat_session")

class ProgressTrack(Base):
    __tablename__ = "progress_tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String)
    progress_percentage = Column(Float)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="progress_tracks")

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    rating = Column(Integer)  # 1-5 stars
    was_helpful = Column(Boolean)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    chat_session = relationship("ChatSession", back_populates="feedback") 