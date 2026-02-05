from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_role
from app.core.roles import ROLE_ADMIN, ROLE_TEACHER
from app.database.current_session import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", response_model=UserResponse)
def create_user(
        data: UserCreate,
        db: Session = Depends(get_db),
        user: User = Depends(require_role(
            ROLE_ADMIN, ROLE_TEACHER
        ))
):
    return UserService.create(db, data)

