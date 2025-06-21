import re
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")
    full_name: str = Field(
        ..., min_length=2, max_length=120, description="User's full name"
    )
    qualification: Optional[str] = Field(
        None, max_length=120, description="User's qualification"
    )
    dob: Optional[date] = Field(None, description="Date of Birth")
    active: bool = Field(True, description="Whether user is active")

    @field_validator("password")
    def validate_password(cls, v):
        password = v
        if len(password) < 8:
            raise ValueError("Password be at least 8 characters long")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError("Password must contain at least one special character")
        return v

    @field_validator("dob")
    def validate_dob(cls, v):
        today = date.today()

        if v > today:
            raise ValueError("Date of birth cannot be in the future")
        return v

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }


class UserResponseSchema(BaseModel):
    id: int
    email: str
    full_name: str
    qualification: Optional[str]
    dob: Optional[date]
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }


class UserUpdateSchema(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=120)
    qualification: Optional[str] = Field(None, max_length=50)
    dob: Optional[date] = None
    active: Optional[bool] = None

    @field_validator("dob")
    def validate_dob(cls, v):
        if v and v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }


class UserListResponseSchema(BaseModel):
    id: int
    email: str
    full_name: str
    qualification: Optional[str]
    active: bool

    class Config:
        form_attributes = True
