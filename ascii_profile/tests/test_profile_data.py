from datetime import date, datetime, timezone
from unittest.mock import patch

import pytest

from ascii_converter.profile_data import (
    PHILIPPINE_TIMEZONE,
    calculate_uptime,
    create_profile,
)


@pytest.mark.parametrize(("as_of", "expected"), [
    (date(2005, 9, 1), "0 years, 0 months, 0 days"),
    (date(2005, 9, 2), "0 years, 0 months, 1 day"),
    (date(2005, 10, 1), "0 years, 1 month, 0 days"),
    (date(2006, 8, 31), "0 years, 11 months, 30 days"),
    (date(2006, 9, 1), "1 year, 0 months, 0 days"),
    (date(2024, 2, 28), "18 years, 5 months, 27 days"),
    (date(2024, 2, 29), "18 years, 5 months, 28 days"),
    (date(2024, 3, 1), "18 years, 6 months, 0 days"),
    (date(2026, 9, 30), "21 years, 0 months, 29 days"),
    (date(2026, 10, 1), "21 years, 1 month, 0 days"),
    (date(2026, 10, 9), "21 years, 1 month, 8 days"),
    (date(2026, 12, 31), "21 years, 3 months, 30 days"),
    (date(2027, 1, 1), "21 years, 4 months, 0 days"),
])
def test_uptime_counts_completed_calendar_years_months_and_days(as_of, expected):
    assert calculate_uptime(as_of) == expected


def test_uptime_rejects_date_before_birth():
    with pytest.raises(ValueError, match="earlier than the birth date"):
        calculate_uptime(date(2005, 8, 31))


def test_profile_uptime_refreshes_at_philippine_midnight():
    instants = iter([
        datetime(2026, 8, 31, 15, 59, tzinfo=timezone.utc),
        datetime(2026, 8, 31, 16, 0, tzinfo=timezone.utc),
    ])
    with patch("ascii_converter.profile_data.datetime") as clock:
        clock.now.side_effect = lambda tz: next(instants).astimezone(tz)
        before_midnight = create_profile()
        after_midnight = create_profile()

    assert before_midnight.uptime == "20 years, 11 months, 30 days"
    assert after_midnight.uptime == "21 years, 0 months, 0 days"
    assert clock.now.call_count == 2
    clock.now.assert_called_with(PHILIPPINE_TIMEZONE)
