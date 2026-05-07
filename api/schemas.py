from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional, List
from datetime import datetime
from uuid import UUID

class User(BaseModel):
    name: str
    id: UUID
    email: EmailStr
    phone: str
    password: str
    role: Literal['teacher', 'student']
    batch_code: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Batch(BaseModel):
    name: str
    year: int = Field(min_length=4, max_length=4)
    schedule: str
    code: str = Field(min_length=6, max_length=6)

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
    batches: List[str]
    created_at: datetime

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: str
    role: Literal['teacher', 'student']
    batch_code: Optional[str] = None

    class Config:
        from_attributes = True