from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    role = Column(String)  # candidate, interviewer, admin
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
    question_type = Column(String)  # technical, behavioral, etc.
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