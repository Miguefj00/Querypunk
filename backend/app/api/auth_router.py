from datetime import datetime

from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.utils.user_utils import get_current_user_from_token
from app.database.current_session import get_db
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.user_repository import UserRepository
from app.models import User
from app.security.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
        request: Request,
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = UserRepository.get_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    SessionRepository.close_active_sessions_by_user(db, user.id)

    session = SessionRepository.create(
        db=db,
        user_id=user.id,
        ip=request.client.host
    )

    user.last_login = datetime.utcnow()
    db.commit()

    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "role_id": user.role_id,
            "session_id": session.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user_from_token),
):
    SessionRepository.close_active_sessions_by_user(db, user.id)

    return {"message": "Logout successful"}
