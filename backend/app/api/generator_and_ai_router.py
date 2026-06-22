from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.database.enums import DifficultyEnum
from app.models import User
from app.services.challenge_generator_service.ai_and_generate_challenge_service import generate_and_store_challenge
from app.utils.role_utils import require_role, ROLE_ADMIN, ROLE_TEACHER

# Automatic challenge generation and AI narrative endpoint
router = APIRouter(
    prefix="/generator-and-ai",
    tags=["Challenges_generator"]
)


@router.post("/generate-challenge/{chapter}")
def generate_and_store(
        chapter: int,
        difficulty: DifficultyEnum,
        db: Session = Depends(get_db),
        current_user: User = Depends(
            require_role([ROLE_ADMIN, ROLE_TEACHER])
        )
):
    """ Generates and stores a new challenge (ADMIN/TEACHER only). """
    return generate_and_store_challenge(
        db,
        chapter,
        difficulty.value,
        current_user
    )



