from datetime import timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import OccupancyLog, OccupancyState, Seat
from app.schemas import OccupancyEventCreate
from app.services.notifications import create_notification


def process_occupancy_event(db: Session, event: OccupancyEventCreate) -> OccupancyLog | None:
    seat = db.get(Seat, event.seat_id)
    if not seat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seat not found")

    event_time = event.event_time.astimezone(timezone.utc) if event.event_time.tzinfo else event.event_time.replace(tzinfo=timezone.utc)

    if seat.current_state == event.state:
        return None

    if event.state == OccupancyState.occupied:
        log = OccupancyLog(seat_id=seat.id, start_time=event_time, duration=0)
        seat.current_state = OccupancyState.occupied
        seat.last_state_change = event_time
        db.add(log)
        create_notification(db, "Seat occupied", f"{seat.seat_name} became occupied.", "info", seat_id=seat.id, camera_id=seat.camera_id)
        db.commit()
        db.refresh(log)
        return log

    open_log = (
        db.query(OccupancyLog)
        .filter(OccupancyLog.seat_id == seat.id, OccupancyLog.end_time.is_(None))
        .order_by(OccupancyLog.start_time.desc())
        .first()
    )
    if open_log:
        open_log.end_time = event_time
        open_log.duration = max(int((event_time - open_log.start_time).total_seconds()), 0)
    seat.current_state = OccupancyState.empty
    seat.last_state_change = event_time
    create_notification(db, "Seat available", f"{seat.seat_name} is now available.", "success", seat_id=seat.id, camera_id=seat.camera_id)
    db.commit()
    if open_log:
        db.refresh(open_log)
    return open_log
