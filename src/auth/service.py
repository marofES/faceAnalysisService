from typing import Annotated
from datetime import datetime, timedelta
from src.auth import models
from src.auth.config import DBSessionDep

from src.auth.schemas import TokenData

from src.auth.dependencies import oauth2_scheme, get_user_by_email, decode_jwt
from src.auth.constants import ACCESS_TOKEN_SECRET_KEY, ACCESS_TOKEN_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES, PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError, encode

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db_session: DBSessionDep) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        permissions = payload.get("permissions")
        if permissions is None:
            raise credentials_exception
        token_data = TokenData(email=email, permissions=permissions)
    except PyJWTError as e:
        raise credentials_exception
    user = await get_user_by_email(db_session, token_data.email)
    if user is None:
        raise credentials_exception
    return user

CurrentUserDep = Annotated[models.User, Depends(get_current_user)]

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt

def create_verification_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt

def create_password_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt
