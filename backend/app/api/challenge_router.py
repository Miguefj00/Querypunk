from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils.role_utils import require_role, ROLE_ADMIN, ROLE_TEACHER
from app.database.current_session import get_db
from app.models import User
from app.schemas.challenge import ChallengeUpdate, ChallengeCreate, ChallengeCreateWithExpectedQuery, \
    ChallengeUpdateWithExpectedQuery
from app.services.challenge_service import ChallengeService
from app.utils.user_utils import get_current_user_from_token

# CRUD operations for challenges
router = APIRouter(prefix="/chapters/{chapter_id}/challenges", tags=["Challenges"])


@router.get("")
def get_challenges(
        chapter_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user_from_token)
):
    """Get all challenges in a chapter"""
    return ChallengeService.get_by_chapter(db, chapter_id, current_user)


@router.get("/{challenge_id}")
def get_challenge(
        chapter_id: int,
        challenge_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user_from_token)
):
    """Get details of a specific challenge"""
    return ChallengeService.get_by_id(db, chapter_id, challenge_id, current_user)


@router.post("", response_model=ChallengeCreateWithExpectedQuery)
def create_challenge(
        chapter_id: int,
        data: ChallengeCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Create challenge (ADMIN/TEACHER only)"""
    return ChallengeService.create(db, chapter_id, data, current_user)


@router.put("/{challenge_id}", response_model=ChallengeUpdateWithExpectedQuery)
def update_challenge(
        chapter_id: int,
        challenge_id: int,
        data: ChallengeUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Update challenge (ADMIN/TEACHER only)"""
    return ChallengeService.update(db, chapter_id, challenge_id, data, current_user)


@router.delete("/{challenge_id}")
def delete_challenge(
        chapter_id: int,
        challenge_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Delete challenge (ADMIN/TEACHER only)"""
    return ChallengeService.delete(db, chapter_id, challenge_id, current_user)
