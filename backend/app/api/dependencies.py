from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.user_repository import UserRepository
from app.models.user import User
from app.security.auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    payload = decode_token(token)

    user = UserRepository.get_by_username(db, payload["sub"])
    if not user:
        raise HTTPException(status_code=401)

    return user


def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        session_id = payload.get("session_id")

        if not username or not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = UserRepository.get_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    session = SessionRepository.get_by_id(db, session_id)

    if not session or session.Logout_time is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )

    if session.User_id != user.Id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session does not belong to user"
        )

    return user


def require_role(*allowed_roles: int):
    def dependency(
            user: User = Depends(get_current_user_from_token)
    ) -> User:
        if user.Role_id not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user

    return dependency

