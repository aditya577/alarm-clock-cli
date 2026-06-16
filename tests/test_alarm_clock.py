import unittest
from datetime import datetime, timedelta

from alarm_clock import parse_alarm_time, seconds_until


class AlarmClockTest(unittest.TestCase):
    def test_parse_absolute_today(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        target = parse_alarm_time("09:15", now)
        self.assertEqual(target, datetime(2026, 6, 16, 9, 15, 0))

    def test_parse_absolute_next_day(self):
        now = datetime(2026, 6, 16, 23, 30, 0)
        target = parse_alarm_time("23:00", now)
        self.assertEqual(target, datetime(2026, 6, 17, 23, 0, 0))

    def test_parse_absolute_seconds(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        target = parse_alarm_time("08:00:30", now)
        self.assertEqual(target, datetime(2026, 6, 16, 8, 0, 30))

    def test_parse_relative_minutes(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        target = parse_alarm_time("+10", now)
        self.assertEqual(target, datetime(2026, 6, 16, 8, 10, 0))

    def test_parse_relative_minutes_with_m(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        target = parse_alarm_time("+5m", now)
        self.assertEqual(target, datetime(2026, 6, 16, 8, 5, 0))

    def test_parse_relative_hours_and_minutes(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        target = parse_alarm_time("+1h30m", now)
        self.assertEqual(target, datetime(2026, 6, 16, 9, 30, 0))

    def test_parse_now(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        target = parse_alarm_time("now", now)
        self.assertEqual(target, now)

    def test_parse_invalid_format(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        with self.assertRaises(ValueError):
            parse_alarm_time("abc", now)

    def test_seconds_until(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        target = datetime(2026, 6, 16, 8, 5, 30)
        self.assertEqual(seconds_until(target, now), 330)

    def test_seconds_until_past(self):
        now = datetime(2026, 6, 16, 8, 0, 0)
        target = datetime(2026, 6, 16, 7, 0, 0)
        self.assertEqual(seconds_until(target, now), 0)


if __name__ == "__main__":
    unittest.main()
