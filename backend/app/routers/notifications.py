from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.models import DeviceToken, Notification, User
from app.schemas import DeviceTokenCreate, NotificationRead

router = APIRouter(tags=["Notifications"])


@router.get("/notifications", response_model=list[NotificationRead])
def list_notifications(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Notification).order_by(Notification.created_at.desc()).limit(100).all()


@router.post("/notifications/device-token", status_code=status.HTTP_201_CREATED)
def register_device_token(payload: DeviceTokenCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    existing = db.query(DeviceToken).filter(DeviceToken.token == payload.token).first()
    if existing:
        existing.user_id = user.id
        existing.platform = payload.platform
    else:
        db.add(DeviceToken(user_id=user.id, token=payload.token, platform=payload.platform))
    db.commit()
    return {"status": "registered"}
