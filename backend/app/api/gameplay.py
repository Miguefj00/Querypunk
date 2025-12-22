from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.schemas.attempt import AttemptCreate

router = APIRouter(prefix="/gameplay", tags=["Gameplay"])

@router.post("/submit-query")
def submit_query(attempt: AttemptCreate, db: Session = Depends(get_db)):
    return {
        "message": "Consulta recibida",
        "challenge_id": attempt.challenge_id,
        "query": attempt.submitted_query
    }
