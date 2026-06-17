from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user, require_roles
from app.models import Camera, Seat, User, UserRole
from app.schemas import SeatCreate, SeatRead

router = APIRouter(tags=["Seats"])


@router.get("/seats", response_model=list[SeatRead])
def list_seats(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Seat).order_by(Seat.id).all()


@router.post("/seat", response_model=SeatRead, status_code=status.HTTP_201_CREATED)
def create_seat(payload: SeatCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.manager))):
    if payload.region_x2 <= payload.region_x1 or payload.region_y2 <= payload.region_y1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Seat region bottom-right must be greater than top-left")
    if not db.get(Camera, payload.camera_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
    seat = Seat(**payload.model_dump())
    db.add(seat)
    db.commit()
    db.refresh(seat)
    return seat
