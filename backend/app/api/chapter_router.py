from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.current_session import get_db
from app.schemas.chapter import *
from app.services.chapter_service import ChapterService
from app.utils.role_utils import require_role
from app.utils.role_utils import ROLE_ADMIN, ROLE_TEACHER
from app.utils.user_utils import get_current_user_from_token

router = APIRouter(prefix="/chapters", tags=["Chapters"])


@router.get("", response_model=list[ChapterResponse])
def get_all_chapters(
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user_from_token)
):
    return ChapterService.get_all(db, current_user)


@router.get("/{chapter_id}", response_model=ChapterResponse)
def get_chapter(
        chapter_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user_from_token)
):
    return ChapterService.get_by_id(db, chapter_id)


@router.post("", response_model=ChapterResponse)
def create_chapter(
        data: ChapterCreate,
        db: Session = Depends(get_db),
        current_user = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    return ChapterService.create(db, data, current_user)


@router.put("/{chapter_id}", response_model=ChapterResponse)
def update_chapter(
        chapter_id: int,
        data: ChapterUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    return ChapterService.update(db, chapter_id, data, current_user)


@router.delete("/{chapter_id}")
def delete_chapter(
        chapter_id: int,
        db: Session = Depends(get_db),
        current_user = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    ChapterService.delete(db, chapter_id, current_user)
    return {"detail": "Chapter deleted successfully"}