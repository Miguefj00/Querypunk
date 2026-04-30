from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.schemas.gameplay import ResetRunRequest
from app.utils.user_utils import get_current_user_from_token
from app.schemas.attempt import AttemptCreate, AttemptResponse
from app.services.gameplay_service import GameplayService

# Entry point for the SQL game engine
router = APIRouter(prefix="/gameplay", tags=["Gameplay"])


@router.post("/submit-query",
             response_model=AttemptResponse,
             response_model_exclude_unset=True)
def submit_query(
        attempt: AttemptCreate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user_from_token)
):
    """
    Core gameplay endpoint:
    - Executes user SQL query
    - Compares with expected solution
    - Stores attempt
    - Calculates score
    - Updates leaderboard
    """
    return GameplayService.submit_query(
        db,
        current_user.id,
        attempt.challenge_id,
        attempt.query
    )


@router.post("/reset-run")
def reset_run(
        data: ResetRunRequest,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user_from_token)
):
    """
    Resets current challenge run:
    - Closes active run WITHOUT scoring
    - Starts a new run
    - Keeps full attempt history
    """
    return GameplayService.reset_run(
        db,
        current_user.id,
        data.challenge_id
    )
