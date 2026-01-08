from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.database.current_session import get_db
from app.schemas.attempt import AttemptCreate, AttemptResponse
from app.models.user import User
from app.services import gameplay_service

router = APIRouter(prefix="/gameplay", tags=["Gameplay"])

@router.post("/submit-query", response_model=AttemptResponse)
def submit_query(
        data: AttemptCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return gameplay_service.process_attempt(db, user, data)

