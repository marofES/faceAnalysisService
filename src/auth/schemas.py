# pydantic models
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    staff = "staff"
    n_user = "n_user"
    guest = "guest"

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.n_user

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    role: RoleEnum

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str