from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.current_session import get_db

from app.utils.user_utils import get_current_user_from_token

from app.models import User

from app.services.analytics_service import (
    AnalyticsService
)

router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)


@router.get("/me")
def get_my_progress(
        db: Session = Depends(get_db),
        current_user: User = Depends(
            get_current_user_from_token
        )
):
    """ Individual progress in game. """
    return AnalyticsService.get_my_progress(
        db,
        current_user.id
    )
