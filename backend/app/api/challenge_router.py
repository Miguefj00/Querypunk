from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.user_utils import get_current_user_from_token
from app.database.current_session import get_db
from app.models import User
from app.schemas.challenge import ChallengeUpdate, ChallengeCreate
from app.services.challenge_service import ChallengeService

router = APIRouter(prefix="/chapters/{chapter_id}/challenges", tags=["Challenges"])


@router.post("")
def create_challenge(
        chapter_id: int,
        data: ChallengeCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    return ChallengeService.create(db, chapter_id, data, current_user)


@router.get("")
def get_challenges(chapter_id: int, db: Session = Depends(get_db)):
    return ChallengeService.get_by_chapter(db, chapter_id)


@router.get("/{challenge_id}")
def get_challenge(
        chapter_id: int,
        challenge_id: int,
        db: Session = Depends(get_db),
):
    return ChallengeService.get_by_id(db, chapter_id, challenge_id)


@router.put("/{challenge_id}")
def update_challenge(
        chapter_id: int,
        challenge_id: int,
        data: ChallengeUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    return ChallengeService.update(db, chapter_id, challenge_id, data, current_user)


@router.delete("/{challenge_id}")
def delete_challenge(
        chapter_id: int,
        challenge_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    return ChallengeService.delete(db, chapter_id, challenge_id, current_user)
