from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SubjectCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Subject name")
    description: Optional[str] = Field(None, description="Subject description")


class SubjectUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = None


class SubjectResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
