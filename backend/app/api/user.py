from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.api.dependencies import require_role, get_current_user_from_token
from app.core.roles import ROLE_ADMIN, ROLE_TEACHER
from app.database.current_session import get_db
from app.database.repositories.user_repository import UserRepository
from app.models import User
from app.schemas.user import UserCreate, UserResponse, UserRead, UserBase
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse)
def create_user(
        data: UserCreate,
        db: Session = Depends(get_db),
        user: User = Depends(require_role(
            ROLE_ADMIN, ROLE_TEACHER
        ))
):
    return UserService.create(db, data)


@router.get(
    "",
    response_model=List[UserBase]
)
def get_users(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    users = UserRepository.get_all(db)

    if current_user.role_id != ROLE_ADMIN:
        users = [u for u in users if u.role_id != ROLE_ADMIN]

    return users


@router.get(
    "/{user_id}",
    response_model=UserRead
)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    user = UserRepository.get_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.role_id == ROLE_ADMIN:
        if current_user.role_id != ROLE_ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions"
            )

    return user


