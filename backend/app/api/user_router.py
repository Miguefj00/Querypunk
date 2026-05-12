from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.utils.user_utils import get_current_user_from_token
from app.utils.role_utils import require_role, ROLE_ADMIN, ROLE_TEACHER
from app.database.current_session import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse, UserRead, UserBase, UserUpdate, ChangePasswordRequest, \
    UserBulkDelete
from app.services.user_service import UserService

# CRUD operations for users and password management
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserBase])
def get_users(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    """ List users. """
    return UserService.get_all(db, current_user)


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)
):
    """ Get user profile. """
    return UserService.get_by_id(db, user_id, current_user)


@router.post("", response_model=UserResponse)
def create_user(
        data: UserCreate,
        db: Session = Depends(get_db),
        user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """ Create user (ADMIN/TEACHER only). """
    return UserService.create(db, data)


@router.put("/change-password", status_code=status.HTTP_200_OK)
def change_password(
        data: ChangePasswordRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    """ Change password of authenticated user. """
    return UserService.change_password(db, current_user, data)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
        user_id: int,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    """ Update own user. """
    return UserService.update(db, user_id, user_update, current_user)


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER])),
):
    """ Delete own user or student user (ADMIN/TEACHER only). """
    return UserService.delete(db, user_id, current_user)


@router.delete("/")
def delete_users(
        data: UserBulkDelete,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER])),
):
    """ Bulk delete own user or student user (ADMIN/TEACHER only). """
    return UserService.delete_bulk(db, data.user_ids, current_user)

