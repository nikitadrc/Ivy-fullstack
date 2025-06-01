from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interviews = relationship("Interview", back_populates="user")
    analytics = relationship("Analytics", back_populates="user")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    candidate_name = Column(String)
    position = Column(String)
    scheduled_time = Column(DateTime)
    duration = Column(Integer)  # in minutes
    interview_type = Column(String)  # technical, behavioral, etc.
    status = Column(String)  # scheduled, completed, cancelled
    notes = Column(Text)
    recording_url = Column(String, nullable=True)
    feedback = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="interviews")
    analysis = relationship("InterviewAnalysis", back_populates="interview", uselist=False)

class InterviewAnalysis(Base):
    __tablename__ = "interview_analyses"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    emotion_data = Column(JSON)  # Timestamped emotion detection results
    speech_data = Column(JSON)  # Speech analysis results
    behavioral_metrics = Column(JSON)  # Body language and behavioral analysis
    technical_assessment = Column(JSON, nullable=True)  # Technical skills assessment
    overall_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interview = relationship("Interview", back_populates="analysis")

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime)
    total_interviews = Column(Integer)
    successful_hires = Column(Integer)
    average_duration = Column(Float)
    success_rate = Column(Float)
    feedback_scores = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="analytics")

class OAuth2Account(Base):
    __tablename__ = "oauth2_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider = Column(String)  # google, github, etc.
    provider_user_id = Column(String)
    access_token = Column(String)
    expires_at = Column(DateTime, nullable=True)
    refresh_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User") 