from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str

    @validator('role')
    def validate_role(cls, v):
        if v not in ['candidate', 'interviewer', 'admin']:
            raise ValueError('Invalid role')
        return v

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Interview schemas
class InterviewBase(BaseModel):
    candidate_id: int
    interviewer_id: int
    position: str
    scheduled_time: datetime
    duration_minutes: int = 60

class InterviewCreate(InterviewBase):
    pass

class InterviewUpdate(BaseModel):
    status: Optional[str]
    feedback: Optional[str]
    materials_url: Optional[str]

    @validator('status')
    def validate_status(cls, v):
        if v not in ['scheduled', 'in_progress', 'completed', 'cancelled']:
            raise ValueError('Invalid status')
        return v

class InterviewResponse(InterviewBase):
    id: int
    status: str
    feedback: Optional[str]
    calendar_event_id: Optional[str]
    meeting_link: Optional[str]
    materials_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# Question schemas
class QuestionBase(BaseModel):
    question_text: str
    question_type: str
    order: int

class QuestionCreate(QuestionBase):
    interview_id: int

class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Response schemas
class ResponseBase(BaseModel):
    response_text: str
    score: Optional[int]
    feedback: Optional[str]

class ResponseCreate(ResponseBase):
    interview_id: int
    question_id: int

class ResponseUpdate(BaseModel):
    score: int
    feedback: str

    @validator('score')
    def validate_score(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('Score must be between 1 and 5')
        return v

class ResponseResponse(ResponseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# File schemas
class FileBase(BaseModel):
    filename: str
    file_type: str
    file_size: int

class FileCreate(FileBase):
    user_id: int
    interview_id: Optional[int]

class FileResponse(FileBase):
    id: int
    file_path: str
    upload_time: datetime

    class Config:
        orm_mode = True

# Composite schemas
class InterviewDetailResponse(InterviewResponse):
    candidate: UserResponse
    interviewer: UserResponse
    questions: List[QuestionResponse]
    responses: List[ResponseResponse]
    files: List[FileResponse]

    class Config:
        orm_mode = True 