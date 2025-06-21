from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator


class QuestionCreateSchema(BaseModel):
    statement: str = Field(..., min_length=1, description="Question statement")
    option1: str = Field(..., min_length=1, description="Option 1")
    option2: str = Field(..., min_length=1, description="Option 2")
    option3: str = Field(..., min_length=1, description="Option 3")
    option4: str = Field(..., min_length=1, description="Option 4")
    correct_option: int = Field(..., gt=1, le=4, description="Correct option (1-4)")

    @field_validator("correct_option")
    def validate_correct_option(cls, v):
        if v not in [1, 2, 3, 4]:
            raise ValidationError("Correct option must be between 1 and 4")
        return v


class QuestionUpdateSchema(BaseModel):
    statement: Optional[str] = Field(None, min_length=1)
    option1: Optional[str] = Field(None, min_length=1)
    option2: Optional[str] = Field(None, min_length=1)
    option3: Optional[str] = Field(None, min_length=1)
    option4: Optional[str] = Field(None, min_length=1)
    correct_option: Optional[int] = Field(None, gt=1, le=4)

    @field_validator("correct_option")
    def validate_correct_option(cls, v):
        if v not in [1, 2, 3, 4]:
            raise ValidationError("Correct option must be between 1 and 4")
        return v


class QuestionResponseSchema(BaseModel):
    id: int
    quiz_id: int
    statement: str
    option1: str
    option2: str
    option3: str
    option4: str
    correct_option: int

    class Config:
        form_attributes = True
