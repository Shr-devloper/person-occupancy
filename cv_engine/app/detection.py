from dataclasses import dataclass

import cv2
from ultralytics import YOLO


@dataclass(frozen=True)
class PersonDetection:
    box: tuple[int, int, int, int]
    confidence: float


class PersonDetector:
    def __init__(self, model_path: str, confidence_threshold: float) -> None:
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect(self, frame) -> list[PersonDetection]:
        results = self.model.predict(frame, verbose=False, conf=self.confidence_threshold, classes=[0])
        detections: list[PersonDetection] = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
                confidence = float(box.conf[0])
                detections.append(PersonDetection(box=(x1, y1, x2, y2), confidence=confidence))
        return detections


def draw_detections(frame, detections: list[PersonDetection]):
    for detection in detections:
        x1, y1, x2, y2 = detection.box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 0), 2)
        cv2.putText(frame, f"person {detection.confidence:.2f}", (x1, max(y1 - 8, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 1)
    return frame
