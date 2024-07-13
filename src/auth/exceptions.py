# module-specific errors
from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
inactive_user_exception = HTTPException(status_code=400, detail="Inactive user")
not_an_admin_exception = HTTPException(status_code=400, detail="Not an admin")
