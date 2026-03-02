from typing import List

from fastapi import Depends, HTTPException
from starlette import status

from app.models import User
from app.utils.user_utils import get_current_user_from_token

ROLE_STUDENT = 1
ROLE_TEACHER = 2
ROLE_ADMIN = 3


def require_role(allowed_roles: List[int]):
    def dependency(
            user: User = Depends(get_current_user_from_token)
    ) -> User:
        if user.role_id not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user

    return dependency
