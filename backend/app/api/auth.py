from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.models.user import User


def get_current_user(db: Session = Depends(get_db)) -> User:
    user: Optional[User] = db.query(User).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )

    return user
