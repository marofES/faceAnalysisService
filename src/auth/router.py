from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import uuid4
from src.auth.config import DBSessionDep
from src.auth.utils import validate_is_authenticated
from src.auth.schemas import User, UserCreate, UserUpdate, EmailVerification, PasswordReset, Token
from src.auth.dependencies import get_user, get_user_by_email,decode_jwt, is_authenticated
from src.auth.constants import ACCESS_TOKEN_EXPIRE_MINUTES

from src.database import get_db_session, sessionmanager

from src.auth.models import User as UserDBModel, Role
from src.auth.service import create_access_token, create_verification_token, create_password_reset_token, CurrentUserDep, get_current_user
#from src.auth.email import send_verification_email, send_password_reset_email
from passlib.context import CryptContext
from datetime import timedelta
from jwt import PyJWTError, encode
from sqlalchemy import select


router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@router.get(
    "/{user_id}",
    response_model=User,
    dependencies=[Depends(validate_is_authenticated)],
)
async def user_details(
    user_id: str,
    db_session: DBSessionDep,
):
    """
    Get any user details
    """
    user = await get_user(db_session, user_id)
    return user


@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db_session: DBSessionDep):
    hashed_password = get_password_hash(user.password)
    new_user = UserDBModel(
        id=str(uuid4())[:6],
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        hashed_password=hashed_password,
        role=Role(user.role)
    )
    db_session.add(new_user)
    await db_session.commit()
    verification_token = create_verification_token(user.email)
    #send_verification_email(user.email, verification_token)
    return new_user

@router.post("/verify-email")
async def verify_email(token: str, db_session: DBSessionDep):
    try:
        payload = decode_jwt(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        user = await get_user_by_email(db_session, email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        user.is_verified = True
        await db_session.commit()
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    return {"message": "Email verified"}

@router.post("/login", response_model=Token)
async def login(user: UserCreate, db_session: DBSessionDep):
    db_user = await get_user_by_email(db_session, user.email)
    if db_user is None or not is_authenticated(db_user, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not db_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email, "permissions": db_user.role.name},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/reset-password", response_model=EmailVerification)
async def reset_password_request(email: str, db_session: DBSessionDep):
    user = await get_user_by_email(db_session, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    password_reset_token = create_password_reset_token(email)
    #send_password_reset_email(email, password_reset_token)
    return {"email": email, "token": password_reset_token}

@router.post("/reset-password/confirm")
async def reset_password_confirm(data: PasswordReset, db_session: DBSessionDep):
    try:
        payload = decode_jwt(data.token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        user = await get_user_by_email(db_session, email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        user.hashed_password = get_password_hash(data.new_password)
        await db_session.commit()
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    return {"message": "Password reset successful"}

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserUpdate, current_user: CurrentUserDep, db_session: DBSessionDep):
    user = await get_user(db_session, user_id)
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    await db_session.commit()
    return user

@router.get("/list", response_model=List[User])
async def list_users(current_user: CurrentUserDep, db_session: DBSessionDep, skip: int = 0, limit: int = 10):
    if current_user.role not in [Role.ADMIN, Role.STAFF]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    users = await db_session.execute(select(UserDBModel).offset(skip).limit(limit))
    return users.scalars().all()

@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: str, current_user: CurrentUserDep, db_session: DBSessionDep):
    user = await get_user(db_session, user_id)
    if current_user.role != Role.ADMIN or user.role == Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    await db_session.delete(user)
    await db_session.commit()
    return user
