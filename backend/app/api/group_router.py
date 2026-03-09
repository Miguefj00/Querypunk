from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.schemas.user import UserInGroupResponse
from app.services.group_service import GroupService
from app.schemas.group import GroupImportResult, GroupResponse, GroupListResponse
from app.utils.role_utils import require_role
from app.utils.role_utils import ROLE_ADMIN, ROLE_TEACHER
from app.models.user import User

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("", response_model=GroupResponse)
def create_group(
        name: str = Form(...),
        description: str = Form(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    group = GroupService.create_group(
        db=db,
        name=name,
        description=description,
        created_by=current_user.id
    )

    return group


@router.post("/{group_id}/upload", response_model=GroupImportResult)
async def upload_students_to_group(
        group_id: int,
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):

    return await GroupService.upload_students_to_group(
        db=db,
        group_id=group_id,
        file=file,
        background_tasks=background_tasks
    )


@router.get("", response_model=List[GroupListResponse])
def get_all_groups(
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    return GroupService.get_all_groups(db)


@router.get("/{group_id}/users", response_model=List[UserInGroupResponse])
def get_group_users(
        group_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    return GroupService.get_group_users(db, group_id)


@router.put("/{group_id}")
def update_group(
        group_id: int,
        name: str = Form(...),
        description: str = Form(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    return GroupService.update_group(
        db=db,
        group_id=group_id,
        name=name,
        description=description,
        current_user=current_user
    )


@router.delete("/{group_id}")
def delete_group(
        group_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    return GroupService.delete_group(
        db=db,
        group_id=group_id,
        current_user=current_user
    )