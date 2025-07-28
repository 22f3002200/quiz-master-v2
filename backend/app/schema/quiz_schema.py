from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class QuizCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=120, description="Quiz title")
    date_of_quiz: date = Field(..., description="Date of quiz")
    scheduled_at: datetime = Field(..., description="Time of quiz")
    duration: int = Field(..., gt=0, description="Duration in minutes")
    remarks: Optional[str] = Field("Easy Peasy", description="Quiz remarks")


class QuizUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    date_of_quiz: Optional[date] = None
    scheduled_at: Optional[datetime] = None
    duration: Optional[int] = Field(None, gt=0)
    remarks: Optional[str] = None


class QuizResponseSchema(BaseModel):
    id: int
    chapter_id: int
    subject_id: int
    title: str
    date_of_quiz: date
    scheduled_at: datetime
    duration: int
    remarks: Optional[str]
    created_at: datetime
    total_marks: float

    class Config:
        from_attributes = True
