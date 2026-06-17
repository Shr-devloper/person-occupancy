from app.seat_region import SeatRegion, person_overlaps_seat


def test_person_overlaps_seat_when_box_intersects_region():
    region = SeatRegion(x1=100, y1=100, x2=300, y2=300)
    assert person_overlaps_seat(region, (150, 150, 280, 280), min_ratio=0.15)


def test_person_does_not_overlap_seat_when_box_is_outside_region():
    region = SeatRegion(x1=100, y1=100, x2=300, y2=300)
    assert not person_overlaps_seat(region, (350, 350, 450, 450), min_ratio=0.15)
