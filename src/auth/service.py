# module-specific business logic
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.auth.constants import SECRET_KEY, ALGORITHM
from src.auth.models import User


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def authenticate_user(self, db: AsyncSession, username: str, password: str):
        async with db.begin() as session:
            result = await session.execute(select(User).filter(User.username == username))
            user = result.scalar_one_or_none()
            if not user:
                return False
            if not self.verify_password(password, user.hashed_password):
                return False
            return user

    async def get_user(self, db: AsyncSession, username: str):
        async with db() as session:
            result = await session.execute(select(User).filter(User.username == username))
            return result.scalar_one_or_none()

