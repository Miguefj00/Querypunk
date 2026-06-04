import unicodedata
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.database.repositories.session_repository import SessionRepository
from app.database.repositories.user_repository import UserRepository
from app.models.user_group import UserGroup
from app.security.auth import decode_token

"""
Authentication helpers and user management utilities.

Includes:
- JWT user extraction
- Username/password generation for bulk imports
- Group assignment helpers
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """
    Extracts and validates the authenticated user from JWT token.

    Checks:
    - Token integrity
    - Active session existence
    - Session ownership

    Returns the authenticated User object.
    Raises HTTP 401 if validation fails.
    """
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


def get_current_session_from_token(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """
    Extracts and validates the authenticated user session from JWT token.

    Checks:
    - Token integrity
    - Active session existence

    Returns the authenticated Session object.
    Raises HTTP 401 if validation fails.
    """
    try:

        payload = decode_token(token)

        session_id = payload.get(
            "session_id"
        )

        if not session_id:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    session = SessionRepository.get_by_id(
        db,
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=401,
            detail="Session not found"
        )

    if session.logout_time is not None:

        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )

    return session


def generate_password_from_identifier(identifier: str) -> str:
    """
    Generates a default password from an external identifier.

    Extracts the last 4 digits of the identifier.
    Used during bulk student import.
    """
    if not identifier:
        raise HTTPException(
            status_code=400,
            detail="Identifier missing in CSV"
        )

    digits = ''.join(filter(str.isdigit, identifier))

    if len(digits) < 4:
        raise HTTPException(status_code=400, detail="Invalid identifier format")
    return digits[-4:]


def generate_username_from_name(nombre: str, apellido: str) -> str:
    """
    Generates a normalized username from first and last name.

    Removes spaces, accents and special characters.
    """
    username = f"{nombre}_{apellido}".lower().replace(" ", "")
    username = unicodedata.normalize("NFKD", username).encode("ascii", "ignore").decode("ascii")
    return username


def assign_user_to_group(db: Session, user_id: int, group_id: int):
    """
    Assigns a user to a group if not already assigned.

    Returns True if relation was created, False if it already existed.
    """
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

    return True
