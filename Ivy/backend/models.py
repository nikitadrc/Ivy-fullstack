from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    selected_role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="user")
    progress = relationship("ProgressTrack", back_populates="user")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # 'user' or 'assistant'
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    question_type = Column(String)

    user = relationship("User", back_populates="messages")
    feedback = relationship("Feedback", back_populates="message")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    rating = Column(Integer)
    was_helpful = Column(Boolean)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    message = relationship("Message", back_populates="feedback")

class ProgressTrack(Base):
    __tablename__ = "progress_tracks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String)
    progress = Column(Float)  # 0 to 1
    last_studied = Column(DateTime, default=datetime.utcnow)
    streak_days = Column(Integer, default=0)

    user = relationship("User", back_populates="progress") 