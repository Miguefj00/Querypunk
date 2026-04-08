from fastapi import APIRouter, Query
from app.services.ai_service.ai_challenge_service import generate_and_store_challenge

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate-challenge/{chapter}")
def generate_and_store(
        chapter: int,
        difficulty: str = Query(..., description="VERY_EASY | EASY | MEDIUM | HARD | EXPERT")
):
    return generate_and_store_challenge(chapter, difficulty)
