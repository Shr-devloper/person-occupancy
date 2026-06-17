from dataclasses import dataclass


@dataclass(frozen=True)
class SeatRegion:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def area(self) -> int:
        return max(self.x2 - self.x1, 0) * max(self.y2 - self.y1, 0)

    def intersection_ratio(self, box: tuple[int, int, int, int]) -> float:
        bx1, by1, bx2, by2 = box
        ix1 = max(self.x1, bx1)
        iy1 = max(self.y1, by1)
        ix2 = min(self.x2, bx2)
        iy2 = min(self.y2, by2)
        intersection = max(ix2 - ix1, 0) * max(iy2 - iy1, 0)
        if self.area == 0:
            return 0.0
        return intersection / self.area


def person_overlaps_seat(region: SeatRegion, box: tuple[int, int, int, int], min_ratio: float = 0.15) -> bool:
    return region.intersection_ratio(box) >= min_ratio
