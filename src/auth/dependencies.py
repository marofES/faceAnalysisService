import jwt
from src.auth.constants import ACCESS_TOKEN_SECRET_KEY, ACCESS_TOKEN_ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from src.auth.models import User as UserDBModel
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def is_authenticated(user, password: str) -> bool:
    if not user or not user.hashed_password:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])

async def get_user(db_session: AsyncSession, user_id: str):
    user = (await db_session.scalars(select(UserDBModel).where(UserDBModel.id == user_id))).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_user_by_email(db_session: AsyncSession, email: str):
    return (await db_session.scalars(select(UserDBModel).where(UserDBModel.email == email))).first()
