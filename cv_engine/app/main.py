import json
import logging
from pathlib import Path

import cv2

from app.backend_client import BackendClient
from app.config import settings
from app.detection import PersonDetector, draw_detections
from app.logger import configure_logging
from app.occupancy import SeatTracker
from app.seat_region import SeatRegion, person_overlaps_seat

logger = logging.getLogger(__name__)


def _camera_source(value: str):
    return int(value) if value.isdigit() else value


def load_seat_config(path: str):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    configure_logging()
    seat_config = load_seat_config(settings.seat_config_path)
    camera_id = int(seat_config["camera_id"])
    seats = {
        int(item["seat_id"]): SeatRegion(**item["region"])
        for item in seat_config["seats"]
    }
    trackers = {seat_id: SeatTracker(seat_id=seat_id) for seat_id in seats}
    detector = PersonDetector(settings.yolo_model, settings.confidence_threshold)
    backend = BackendClient(settings.backend_url)

    capture = cv2.VideoCapture(_camera_source(settings.camera_source))
    if not capture.isOpened():
        raise RuntimeError(f"Camera source could not be opened: {settings.camera_source}")

    logger.info("CV engine started for camera_id=%s seats=%s", camera_id, list(seats.keys()))
    while True:
        ok, frame = capture.read()
        if not ok:
            logger.warning("Camera frame read failed")
            continue

        detections = detector.detect(frame)
        for seat_id, region in seats.items():
            matching_confidences = [d.confidence for d in detections if person_overlaps_seat(region, d.box)]
            has_person = bool(matching_confidences)
            transition = trackers[seat_id].update(
                has_person=has_person,
                occupied_threshold=settings.occupied_frames_threshold,
                empty_threshold=settings.empty_frames_threshold,
            )
            if transition:
                state, event_time = transition
                backend.send_occupancy_event(
                    seat_id=seat_id,
                    camera_id=camera_id,
                    state=state.value,
                    event_time=event_time,
                    confidence=max(matching_confidences) if matching_confidences else None,
                )

            cv2.rectangle(frame, (region.x1, region.y1), (region.x2, region.y2), (255, 165, 0), 2)
            cv2.putText(frame, f"seat {seat_id}: {trackers[seat_id].state.value}", (region.x1, max(region.y1 - 10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)

        draw_detections(frame, detections)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
