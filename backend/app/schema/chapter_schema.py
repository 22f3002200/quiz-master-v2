from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChapterCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Chapter name")
    description: Optional[str] = Field(None, description="Chapter description")


class ChapterUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = None


class ChapterResponseSchema(BaseModel):
    id: int
    subject_id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        form_attributes = True
