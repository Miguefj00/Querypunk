from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.models import User
from app.services.analytics_service import AnalyticsService
from app.utils.role_utils import require_role, ROLE_ADMIN, ROLE_TEACHER

# Responsible for exposing learning analytics
router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def get_overview(
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Returns global platform analytics (ADMIN/TEACHER only)"""
    return AnalyticsService.get_overview(db)


@router.get("/challenges")
def get_challenges_analytics(
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Returns analytics aggregated per challenge (ADMIN/TEACHER only)"""
    return AnalyticsService.get_challenges_analytics(db)


@router.get("/users/{user_id}")
def get_user_analytics(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Returns analytics dashboard for a specific user (ADMIN/TEACHER only)"""
    return AnalyticsService.get_user_dashboard(db, user_id)


@router.get("/student/{user_id}/attempts")
def get_student_attempts_history(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role([ROLE_ADMIN, ROLE_TEACHER]))
):
    """Complete track record of queries executed by a student in each challenge (ADMIN/TEACHER only)"""
    return AnalyticsService.get_student_attempts_history(db, user_id)

