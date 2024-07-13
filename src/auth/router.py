from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import schemas, service, dependencies
from src.database import get_session
from src.auth.constants import RoleEnum

router = APIRouter()

@router.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = await service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await service.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.Login, db: AsyncSession = Depends(get_session)):
    user = await service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token(data={"sub": user.username})
    refresh_token = service.create_refresh_token(data={"sub": user.username})
    return schemas.Token(access_token=access_token, refresh_token=refresh_token)

@router.post("/logout")
async def logout_user(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    # For simplicity, we are not implementing server-side token invalidation
    return {"message": "Successfully logged out"}

@router.post("/token/refresh", response_model=schemas.Token)
async def refresh_access_token(refresh_token: str, db: AsyncSession = Depends(get_session)):
    username = service.verify_refresh_token(refresh_token)
    user = await service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = service.create_access_token(data={"sub": user.username})
    return schemas.Token(access_token=access_token, refresh_token=refresh_token)

@router.get("/users/", response_model=list[schemas.User])
async def get_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session), current_user: schemas.User = Depends(dependencies.get_current_active_admin)):
    users = await service.get_users(db, skip=skip, limit=limit)
    return users
