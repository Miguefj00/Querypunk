from fastapi import APIRouter
from app.services.ai_service.ai_challenge_service import generate_and_store_challenge

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate-challenge/{chapter}")
def generate_and_store(chapter:int):
    return generate_and_store_challenge(chapter)
