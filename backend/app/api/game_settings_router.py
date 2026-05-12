from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.schemas.game_settings import GameSettingsUpdate, GameSettingsResponse
from app.services.game_settings_service import GameSettingsService
from app.utils.role_utils import require_role, ROLE_ADMIN, ROLE_TEACHER
from app.models import User

router = APIRouter(prefix="/game-settings", tags=["Game Settings"])


@router.get("/", response_model=GameSettingsResponse)
def get_settings(
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """ Get game settings (ADMIN/TEACHER). """
    return GameSettingsService.get_settings(db)


@router.put("/", response_model=GameSettingsResponse)
def update_settings(
        payload: GameSettingsUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """ Update game settings (ADMIN/TEACHER). """
    return GameSettingsService.update_settings(db, payload)