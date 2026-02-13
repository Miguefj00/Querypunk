from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.api.dependencies import require_role, get_current_user_from_token
from app.core.roles import ROLE_ADMIN, ROLE_TEACHER
from app.database.current_session import get_db
from app.database.repositories.user_repository import UserRepository
from app.models import User
from app.schemas.user import UserCreate, UserResponse, UserRead, UserBase, UserUpdate
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
        user_id: int,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    is_admin = current_user.role_id == ROLE_ADMIN

    if not is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own user"
        )

    updated_user = UserRepository.update(db, user, user_update)
    return updated_user


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    if current_user.role_id != ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete users"
        )

    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot delete itself"
        )

    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    UserRepository.delete(db, user)

    return {"detail": "User deleted successfully"}

