from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import DashboardAnalytics
from app.services.analytics import dashboard_analytics

router = APIRouter(tags=["Analytics"])


@router.get("/analytics/dashboard", response_model=DashboardAnalytics)
def dashboard(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return dashboard_analytics(db)
