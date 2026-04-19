from fastapi import APIRouter, Depends

from app.database.enums import DifficultyEnum
from app.models import User
from app.services.challenge_generator_service.ai_and_generate_challenge_service import generate_and_store_challenge
from app.utils.role_utils import require_role, ROLE_ADMIN, ROLE_TEACHER

router = APIRouter(prefix="/generator-and-ai", tags=["Challenges_generator"])


@router.post("/generate-challenge/{chapter}")
def generate_and_store(
        chapter: int,
        difficulty: DifficultyEnum,
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    return generate_and_store_challenge(chapter, difficulty.value)