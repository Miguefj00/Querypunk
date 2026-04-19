from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.utils.user_utils import get_current_user_from_token
from app.schemas.attempt import AttemptCreate, AttemptResponse
from app.services.gameplay_service import GameplayService

router = APIRouter(prefix="/gameplay", tags=["Gameplay"])


@router.post("/submit-query",
             response_model=AttemptResponse,
             response_model_exclude_unset=True)
def submit_query(
        attempt: AttemptCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user_from_token)
):
    return GameplayService.submit_query(
        db,
        current_user.id,
        attempt.challenge_id,
        attempt.query
    )


