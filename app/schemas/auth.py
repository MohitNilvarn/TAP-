from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str  # "student" or "teacher"
    year: Optional[str] = None  # <--- ADD THIS. It allows "FE", "SE", etc.

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: str