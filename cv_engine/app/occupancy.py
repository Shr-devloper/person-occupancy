from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class OccupancyState(str, Enum):
    occupied = "occupied"
    empty = "empty"


@dataclass
class SeatTracker:
    seat_id: int
    state: OccupancyState = OccupancyState.empty
    occupied_frames: int = 0
    empty_frames: int = 0

    def update(self, has_person: bool, occupied_threshold: int, empty_threshold: int) -> tuple[OccupancyState, datetime] | None:
        if has_person:
            self.occupied_frames += 1
            self.empty_frames = 0
        else:
            self.empty_frames += 1
            self.occupied_frames = 0

        if self.state == OccupancyState.empty and self.occupied_frames >= occupied_threshold:
            self.state = OccupancyState.occupied
            return self.state, datetime.now(timezone.utc)

        if self.state == OccupancyState.occupied and self.empty_frames >= empty_threshold:
            self.state = OccupancyState.empty
            return self.state, datetime.now(timezone.utc)

        return None
