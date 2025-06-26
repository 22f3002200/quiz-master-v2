import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")


class RegisterSchema(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")
    full_name: str = Field(
        ..., min_length=2, max_length=120, description="User's full name"
    )
    qualification: Optional[str] = Field(
        None, max_length=50, description="User's qualification"
    )
    dob: Optional[date] = Field(None, description="Date of Birth")

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


class RefreshToken(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")


class ChangePasswordSchema(BaseModel):
    current_password: str = Field(..., description="Current Password")
    new_password: str = Field(..., description="New Password")

    @field_validator("new_password")
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
