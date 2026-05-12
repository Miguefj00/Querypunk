from typing import List
from fastapi import Depends, HTTPException
from starlette import status

from app.models import User
from app.utils.user_utils import get_current_user_from_token

"""
Role-based access control utilities.

Provides dependency helpers used by FastAPI endpoints
to restrict access based on user role.
"""

ROLE_STUDENT = 1
ROLE_TEACHER = 2
ROLE_ADMIN = 3


def require_role(allowed_roles: List[int]):
    """
    FastAPI dependency factory for role-based authorization.

    Usage example:
        @router.get("/analytics", dependencies=[Depends(require_role([ROLE_TEACHER]))])

    Ensures the authenticated user has one of the allowed roles.
    Raises HTTP 403 if the user lacks permissions.
    """
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
