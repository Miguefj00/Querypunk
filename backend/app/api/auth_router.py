from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from app.utils.user_utils import get_current_user_from_token
from app.database.current_session import get_db
from app.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):

    return AuthService.login(
        db=db,
        username=form_data.username,
        password=form_data.password,
        ip=request.client.host
    )


@router.post("/logout")
def logout(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user_from_token),
):

    return AuthService.logout(
        db=db,
        user_id=user.id
    )