import timetable
from datetime import date


def test_not_get_lessons():
    assert timetable.get_lessons_for_day(date(2022, 2, 22)) is None


def test_get_lessons():
    assert timetable.get_lessons_for_day(date(2022, 2, 25)) == [{'name': 'ФМ и ИА', 'time': '9:45', 'group': None, 'online': False},
                                                                 {'name': 'АБД', 'time': '13:25', 'group': None, 'online': False},
                                                                 {'name': 'ИС УПК', 'time': '15:10', 'group': None, 'online': False},
                                                                 {'name': 'РИКТ и ОП', 'time': '16:55', 'group': None, 'online': False},
                                                                 {'name': 'ИС УПК', 'time': '18:40', 'group': 2, 'online': False}]




