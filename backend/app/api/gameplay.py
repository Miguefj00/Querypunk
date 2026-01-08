from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.current_session import get_db
from app.schemas.attempt import AttemptCreate, AttemptResponse
from app.services.gameplay_service import GameplayService

router = APIRouter(prefix="/gameplay", tags=["Gameplay"])

@router.post("/submit-query", response_model=AttemptResponse)
def submit_query(
        data: AttemptCreate,
        db: Session = Depends(get_db)
):
    # Temporary user
    user_id = 1

    return GameplayService.process_attempt(db, user_id, data)
