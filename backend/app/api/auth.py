from fastapi import Depends, Header, HTTPException, status, APIRouter
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.current_session import get_db
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.user_repository import UserRepository
from app.schemas.user import LoginRequest
from app.security.auth import verify_password, create_access_token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(
        data: LoginRequest,
        request: Request,
        db: Session = Depends(get_db)
):
    user, session = AuthService.login(
        db,
        data.username,
        data.password,
        request
    )

    return {
        "session_id": session.Id,
        "user_id": user.Id,
        "role_id": user.Role_id
    }

@router.post("/login-token")
def login_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = UserRepository.get_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.Password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={"sub": user.Username, "role_id": user.Role_id}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(
        db: Session = Depends(get_db),
        session_id: int = Header(...)
):
    session = SessionRepository.get_by_id(db, session_id)

    if session is None or session.Logout_time is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )

    SessionRepository.close(db, session)

    return {"message": "Logout successful"}
