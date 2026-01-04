from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str 

# FIX: Ensure 'role' is listed here!
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: str   # <--- If this is missing, you get a 422 Error