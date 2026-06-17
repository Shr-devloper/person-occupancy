from app.occupancy import OccupancyState, SeatTracker


def test_tracker_transitions_to_occupied_after_threshold():
    tracker = SeatTracker(seat_id=1)

    assert tracker.update(has_person=True, occupied_threshold=2, empty_threshold=2) is None
    transition = tracker.update(has_person=True, occupied_threshold=2, empty_threshold=2)

    assert transition is not None
    state, _ = transition
    assert state == OccupancyState.occupied


def test_tracker_transitions_to_empty_after_threshold():
    tracker = SeatTracker(seat_id=1, state=OccupancyState.occupied)

    assert tracker.update(has_person=False, occupied_threshold=2, empty_threshold=2) is None
    transition = tracker.update(has_person=False, occupied_threshold=2, empty_threshold=2)

    assert transition is not None
    state, _ = transition
    assert state == OccupancyState.empty
