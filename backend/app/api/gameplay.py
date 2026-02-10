from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.api.dependencies import get_current_user_from_token
from app.schemas.attempt import AttemptCreate, AttemptResponse
from app.models.user import User
from app.services.gameplay_service import GameplayService

router = APIRouter(prefix="/gameplay", tags=["Gameplay"])


@router.post("/submit-query", response_model=AttemptResponse)
def submit_query(
        data: AttemptCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user_from_token)
):
    return GameplayService.process_attempt(db, user.Id, data)


