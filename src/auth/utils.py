# any other non-business logic functions
from src.auth import models
from src.auth.service import CurrentUserDep

async def validate_is_authenticated(
    current_user: CurrentUserDep,
) -> models.User:
    """
    This just returns as the CurrentUserDep dependency already throws if there is an issue with the auth token.
    """
    return current_user


