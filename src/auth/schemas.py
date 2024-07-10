from pydantic import BaseModel, ConfigDict, EmailStr, Field
from enum import Enum as PyEnum

class Role(PyEnum):
    ADMIN = 1
    STAFF = 2
    USER = 3
    GUEST = 4

class UserBase(BaseModel):
    id: str
    username: str
    slug: str
    email: EmailStr
    first_name: str
    last_name: str
    is_superuser: bool = False
    is_verified: bool = False
    role: int

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: str
    role: int

class UserUpdate(BaseModel):
    first_name: str
    last_name: str

class User(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    permissions: str = "user"

class EmailVerification(BaseModel):
    email: EmailStr
    token: str

class PasswordReset(BaseModel):
    email: EmailStr
    token: str
    new_password: str = Field(..., min_length=6)
