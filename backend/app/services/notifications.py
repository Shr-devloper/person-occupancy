import logging
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, messaging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import DeviceToken, Notification

logger = logging.getLogger(__name__)


@lru_cache
def _firebase_app():
    if not settings.fcm_credentials_path:
        return None
    if firebase_admin._apps:
        return firebase_admin.get_app()
    cred = credentials.Certificate(settings.fcm_credentials_path)
    return firebase_admin.initialize_app(cred)


def create_notification(
    db: Session,
    title: str,
    message: str,
    severity: str = "info",
    seat_id: int | None = None,
    camera_id: int | None = None,
) -> Notification:
    notification = Notification(title=title, message=message, severity=severity, seat_id=seat_id, camera_id=camera_id)
    db.add(notification)
    return notification


def send_push_to_all(db: Session, title: str, message: str, data: dict[str, str] | None = None) -> int:
    app = _firebase_app()
    if app is None:
        logger.info("FCM credentials not configured; push skipped")
        return 0
    tokens = [row.token for row in db.query(DeviceToken).all()]
    if not tokens:
        return 0
    multicast = messaging.MulticastMessage(
        tokens=tokens,
        notification=messaging.Notification(title=title, body=message),
        data=data or {},
    )
    response = messaging.send_each_for_multicast(multicast)
    logger.info("Sent FCM push: success=%s failure=%s", response.success_count, response.failure_count)
    return response.success_count
