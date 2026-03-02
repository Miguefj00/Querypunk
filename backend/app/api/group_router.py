from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.services.group_service import GroupService
from app.schemas.group import GroupImportResult, GroupResponse
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
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):

    return await GroupService.upload_students_to_group(
        db=db,
        group_id=group_id,
        file=file
    )
