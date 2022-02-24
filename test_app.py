import pytest
import timetable
from datetime import datetime, date


days_off = ['Tuesday']


def test_get_lessons():
    d = date(2022, 2, 24)
    if d.strftime("%A") in days_off:
        assert timetable.get_lessons_for_day(d) is None
    else:
        assert timetable.get_lessons_for_day(d) is not None


