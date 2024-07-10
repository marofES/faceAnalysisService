from src.auth.config import DBSessionDep
from src.auth.utils import validate_is_authenticated
from src.auth.schemas import User
from src.auth.dependencies import get_user
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)
@router.get(
    "/{user_id}",
    response_model=User,
    dependencies=[Depends(validate_is_authenticated)],
)
async def user_details(
    user_id: int,
    db_session: DBSessionDep,
):
    """
    Get any user details
    """
    user = await get_user(db_session, user_id)
    return user