from fastapi import APIRouter

from app.database.enums import DifficultyEnum
from app.services.challenge_generator_service.ai_and_generate_challenge_service import generate_and_store_challenge

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/ai/generate-challenge/{chapter}")
def generate_and_store(
        chapter: int,
        difficulty: DifficultyEnum
):
    return generate_and_store_challenge(chapter, difficulty.value)
