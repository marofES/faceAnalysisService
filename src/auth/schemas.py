from pydantic import BaseModel, EmailStr
from typing import Optional
from src.auth.constants import RoleEnum

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    role: RoleEnum
    is_active: bool = True
    is_verified: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    username: Optional[str] = None
