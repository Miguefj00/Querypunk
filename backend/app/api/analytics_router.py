from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.current_session import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    return AnalyticsService.get_overview(db)


@router.get("/challenges")
def get_challenges_analytics(db: Session = Depends(get_db)):
    return AnalyticsService.get_challenges_analytics(db)


@router.get("/users/{user_id}")
def get_user_analytics(user_id: int, db: Session = Depends(get_db)):
    return AnalyticsService.get_user_dashboard(db, user_id)

