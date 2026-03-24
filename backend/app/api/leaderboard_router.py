from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.current_session import get_db
from app.services.leaderboard_service import LeaderboardService
from app.schemas.leaderboard import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/challenge/{challenge_id}", response_model=List[LeaderboardEntry])
def get_challenge_leaderboard(challenge_id: int, db: Session = Depends(get_db)):
    return LeaderboardService.get_challenge_leaderboard(db, challenge_id)


@router.get("/chapter/{chapter_id}", response_model=List[LeaderboardEntry])
def get_chapter_leaderboard(chapter_id: int, db: Session = Depends(get_db)):
    return LeaderboardService.get_chapter_leaderboard(db, chapter_id)


@router.get("/global", response_model=List[LeaderboardEntry])
def get_global_leaderboard(db: Session = Depends(get_db)):
    return LeaderboardService.get_global_leaderboard(db)