from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.user_repository import UserRepository
from app.models.user_group import UserGroup
from app.security.auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        session_id = payload.get("session_id")

        if not user_id or not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = UserRepository.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    session = SessionRepository.get_by_id(db, session_id)

    if not session or session.logout_time is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )

    if session.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session does not belong to user"
        )

    return user


def generate_password_from_identifier(identifier: str) -> str:
    digits = ''.join(filter(str.isdigit, identifier))
    if len(digits) < 4:
        raise HTTPException(status_code=400, detail="Invalid identifier format")
    return digits[-4:]


def generate_username_from_name(nombre: str, apellido: str) -> str:
    username = f"{nombre}_{apellido}".lower().replace(" ", "")
    return username


def assign_user_to_group(db: Session, user_id: int, group_id: int):
    existing = (
        db.query(UserGroup)
        .filter_by(user_id=user_id, group_id=group_id)
        .first()
    )

    if existing:
        return False

    relation = UserGroup(
        user_id=user_id,
        group_id=group_id
    )

    db.add(relation)
    db.commit()

    return True
