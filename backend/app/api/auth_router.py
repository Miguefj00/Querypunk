from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from app.utils.user_utils import get_current_session_from_token
from app.database.current_session import get_db

# Router responsible for authentication and session management
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    """ OAuth2 login → validates credentials and creates DB session. """
    return AuthService.login(
        db=db,
        username=form_data.username,
        password=form_data.password,
        ip=request.client.host
    )


@router.post("/logout")
def logout(
        current_session = Depends(
            get_current_session_from_token
        ),
        db: Session = Depends(get_db)
):
    """ Closes user active session and logouts. """
    return AuthService.logout(
        db,
        current_session.id
    )
