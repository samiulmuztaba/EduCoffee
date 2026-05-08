from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional, List
from datetime import datetime
from uuid import UUID

class User(BaseModel):
    name: str
    id: Optional[UUID] = None
    email: EmailStr
    center_name: Optional[str] = None
    phone: str
    password: str
    role: Literal['teacher', 'student']
    batch_code: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Batch(BaseModel):
    name: str
    year: str 
    schedule: str
    code: str = Field(min_length=6, max_length=6)
    teacher_id: str

class StudentScore(BaseModel):
    name: str
    marks: Optional[float] = None
    remarks: Optional[str] = ''
    absent: bool
    seen_by_guardian: bool

class Result(BaseModel):
    title: str
    description: Optional[str] 
    total_marks: int 
    batch_code: str = Field(min_length=6, max_length=6)
    scores: List[StudentScore]

class Notice(BaseModel):
    text: str
    teacher_id: str
    batches: Optional[List[str]] = None
    created_at: datetime

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    center_name: Optional[str] = None
    phone: str
    role: Literal['teacher', 'student']
    batch_code: Optional[str] = None

    class Config:
        from_attributes = True