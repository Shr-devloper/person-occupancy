from collections import defaultdict
from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Camera, CameraStatus, OccupancyLog, OccupancyState, Seat
from app.schemas import AnalyticsPoint, DashboardAnalytics, SeatUsage

SECONDS_PER_DAY = 24 * 60 * 60


def _date_bounds(day: date) -> tuple[datetime, datetime]:
    start = datetime.combine(day, time.min, tzinfo=timezone.utc)
    end = start + timedelta(days=1)
    return start, end


def _overlap_seconds(log: OccupancyLog, start: datetime, end: datetime) -> int:
    log_end = log.end_time or datetime.now(timezone.utc)
    overlap_start = max(log.start_time, start)
    overlap_end = min(log_end, end)
    if overlap_end <= overlap_start:
        return 0
    return int((overlap_end - overlap_start).total_seconds())


def occupied_seconds_between(db: Session, start: datetime, end: datetime, seat_id: int | None = None) -> int:
    query = db.query(OccupancyLog).filter(OccupancyLog.start_time < end).filter(
        (OccupancyLog.end_time.is_(None)) | (OccupancyLog.end_time > start)
    )
    if seat_id is not None:
        query = query.filter(OccupancyLog.seat_id == seat_id)
    return sum(_overlap_seconds(log, start, end) for log in query.all())


def daily_analytics(db: Session, target_day: date) -> AnalyticsPoint:
    start, end = _date_bounds(target_day)
    occupied = occupied_seconds_between(db, start, end)
    percentage = round((occupied / SECONDS_PER_DAY) * 100, 2)
    return AnalyticsPoint(label=target_day.isoformat(), occupied_seconds=occupied, occupancy_percentage=percentage)


def range_daily_analytics(db: Session, start_day: date, days: int) -> list[AnalyticsPoint]:
    return [daily_analytics(db, start_day + timedelta(days=offset)) for offset in range(days)]


def weekly_analytics(db: Session, target_day: date) -> list[AnalyticsPoint]:
    week_start = target_day - timedelta(days=target_day.weekday())
    return range_daily_analytics(db, week_start, 7)


def monthly_analytics(db: Session, target_day: date) -> list[AnalyticsPoint]:
    month_start = target_day.replace(day=1)
    next_month = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1)
    days = (next_month - month_start).days
    return range_daily_analytics(db, month_start, days)


def yearly_analytics(db: Session, year: int) -> list[AnalyticsPoint]:
    points = []
    for month in range(1, 13):
        start = datetime(year, month, 1, tzinfo=timezone.utc)
        end = datetime(year + (month == 12), 1 if month == 12 else month + 1, 1, tzinfo=timezone.utc)
        occupied = occupied_seconds_between(db, start, end)
        denominator = int((end - start).total_seconds())
        points.append(
            AnalyticsPoint(
                label=f"{year}-{month:02d}",
                occupied_seconds=occupied,
                occupancy_percentage=round((occupied / denominator) * 100, 2) if denominator else 0,
            )
        )
    return points


def peak_usage_hours(db: Session, target_day: date) -> list[AnalyticsPoint]:
    start, _ = _date_bounds(target_day)
    points = []
    for hour in range(24):
        hour_start = start + timedelta(hours=hour)
        hour_end = hour_start + timedelta(hours=1)
        occupied = occupied_seconds_between(db, hour_start, hour_end)
        points.append(
            AnalyticsPoint(label=f"{hour:02d}:00", occupied_seconds=occupied, occupancy_percentage=round((occupied / 3600) * 100, 2))
        )
    return sorted(points, key=lambda item: item.occupied_seconds, reverse=True)[:5]


def seat_usage(db: Session, start: datetime, end: datetime, ascending: bool = False) -> list[SeatUsage]:
    rows = db.query(Seat).all()
    usage = [
        SeatUsage(seat_id=seat.id, seat_name=seat.seat_name, occupied_seconds=occupied_seconds_between(db, start, end, seat.id))
        for seat in rows
    ]
    return sorted(usage, key=lambda item: item.occupied_seconds, reverse=not ascending)[:5]


def dashboard_analytics(db: Session) -> DashboardAnalytics:
    today = datetime.now(timezone.utc).date()
    day_start, day_end = _date_bounds(today)
    total_seats = db.query(func.count(Seat.id)).scalar() or 0
    occupied_seats = db.query(func.count(Seat.id)).filter(Seat.current_state == OccupancyState.occupied).scalar() or 0
    camera_counts = defaultdict(int)
    for status, count in db.query(Camera.status, func.count(Camera.id)).group_by(Camera.status).all():
        camera_counts[status.value if isinstance(status, CameraStatus) else str(status)] = count
    occupied_today = occupied_seconds_between(db, day_start, day_end)
    return DashboardAnalytics(
        total_seats=total_seats,
        occupied_seats=occupied_seats,
        available_seats=max(total_seats - occupied_seats, 0),
        occupancy_percentage=round((occupied_today / SECONDS_PER_DAY) * 100, 2),
        camera_status=dict(camera_counts),
        daily=[daily_analytics(db, today)],
        weekly=weekly_analytics(db, today),
        monthly=monthly_analytics(db, today),
        peak_usage_hours=peak_usage_hours(db, today),
        most_used_seats=seat_usage(db, day_start, day_end),
        least_used_seats=seat_usage(db, day_start, day_end, ascending=True),
    )
