import logging
from datetime import datetime

import requests

logger = logging.getLogger(__name__)


class BackendClient:
    def __init__(self, backend_url: str, timeout_seconds: int = 5) -> None:
        self.backend_url = backend_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def send_occupancy_event(self, seat_id: int, camera_id: int, state: str, event_time: datetime, confidence: float | None = None) -> None:
        payload = {
            "seat_id": seat_id,
            "camera_id": camera_id,
            "state": state,
            "event_time": event_time.isoformat(),
            "confidence": confidence,
        }
        try:
            response = requests.post(f"{self.backend_url}/occupancy/events", json=payload, timeout=self.timeout_seconds)
            response.raise_for_status()
            logger.info("Sent occupancy event: %s", payload)
        except requests.RequestException:
            logger.exception("Failed to send occupancy event; event will be visible in logs for replay")
