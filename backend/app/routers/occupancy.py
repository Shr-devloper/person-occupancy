from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models import OccupancyLog, User
from app.schemas import AnalyticsPoint, OccupancyEventCreate, OccupancyLogRead
from app.services.analytics import daily_analytics, monthly_analytics, weekly_analytics, yearly_analytics
from app.services.occupancy import process_occupancy_event

router = APIRouter(tags=["Occupancy"])


@router.get("/occupancy", response_model=list[OccupancyLogRead])
def list_occupancy(
    seat_id: int | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(OccupancyLog).order_by(OccupancyLog.start_time.desc())
    if seat_id is not None:
        query = query.filter(OccupancyLog.seat_id == seat_id)
    return query.limit(limit).all()


@router.post("/occupancy/events", response_model=OccupancyLogRead | None)
def create_occupancy_event(payload: OccupancyEventCreate, db: Session = Depends(get_db)):
    # Raspberry Pi devices call this endpoint. In production place it behind mTLS, VPN, or a device API key gateway.
    return process_occupancy_event(db, payload)


@router.get("/occupancy/daily", response_model=AnalyticsPoint)
def get_daily(day: date | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return daily_analytics(db, day or date.today())


@router.get("/occupancy/weekly", response_model=list[AnalyticsPoint])
def get_weekly(day: date | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return weekly_analytics(db, day or date.today())


@router.get("/occupancy/monthly", response_model=list[AnalyticsPoint])
def get_monthly(day: date | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return monthly_analytics(db, day or date.today())


@router.get("/occupancy/yearly", response_model=list[AnalyticsPoint])
def get_yearly(year: int | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return yearly_analytics(db, year or date.today().year)
