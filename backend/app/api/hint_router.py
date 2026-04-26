from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.utils.role_utils import require_role, ROLE_ADMIN, ROLE_TEACHER
from app.models import User
from app.schemas.hint import HintCreate, HintUpdate, HintResponse
from app.services.hint_service import HintService
from app.utils.user_utils import get_current_user_from_token

# CRUD operations for hints
router = APIRouter(
    prefix="/chapters/{chapter_id}/challenges/{challenge_id}/hints",
    tags=["Hints"]
)


@router.get("", response_model=list[HintResponse])
def get_hints(
        chapter_id: int,
        challenge_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user_from_token)
):
    """Get all hints for a challenge"""
    return HintService.get_by_challenge(db, chapter_id, challenge_id, current_user)


@router.get("/{hint_id}", response_model=HintResponse)
def get_hint(
        chapter_id: int,
        challenge_id: int,
        hint_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user_from_token)
):
    """Get a specific hint"""
    return HintService.get_by_id(db, chapter_id, challenge_id, hint_id, current_user)


@router.post("", response_model=HintResponse)
def create_hint(
        chapter_id: int,
        challenge_id: int,
        data: HintCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Create hint (ADMIN/TEACHER only)"""
    return HintService.create(db, chapter_id, challenge_id, data, current_user)


@router.put("/{hint_id}", response_model=HintResponse)
def update_hint(
        chapter_id: int,
        challenge_id: int,
        hint_id: int,
        data: HintUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Update hint (ADMIN/TEACHER only)"""
    return HintService.update(db, chapter_id, challenge_id, hint_id, data, current_user)


@router.delete("/{hint_id}")
def delete_hint(
        chapter_id: int,
        challenge_id: int,
        hint_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Delete hint (ADMIN/TEACHER only)"""
    return HintService.delete(db, chapter_id, challenge_id, hint_id, current_user)
