from datetime import datetime, timezone

from app.models import OccupancyLog
from app.services.analytics import _overlap_seconds


def test_overlap_seconds_clips_log_to_requested_window():
    log = OccupancyLog(
        seat_id=1,
        start_time=datetime(2026, 6, 17, 9, 0, tzinfo=timezone.utc),
        end_time=datetime(2026, 6, 17, 11, 30, tzinfo=timezone.utc),
        duration=9000,
    )
    start = datetime(2026, 6, 17, 10, 0, tzinfo=timezone.utc)
    end = datetime(2026, 6, 17, 12, 0, tzinfo=timezone.utc)
    assert _overlap_seconds(log, start, end) == 5400
