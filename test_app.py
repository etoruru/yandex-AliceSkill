import app
import sayings
import timetable

from datetime import date

import time_machine


def test_not_get_lessons():
    assert timetable.get_lessons_for_day(date(2022, 2, 22)) is None, "Should be None"


def test_get_lessons():
    assert timetable.get_lessons_for_day(date(2022, 2, 25)) == \
           [{'name': 'ФМ и ИА', 'time': '9:45', 'group': None, 'online': False},
            {'name': 'АБД', 'time': '13:25', 'group': None, 'online': False},
            {'name': 'ИС УПК', 'time': '15:10', 'group': None, 'online': False},
            {'name': 'РИКТ и ОП', 'time': '16:55', 'group': None, 'online': False},
            {'name': 'ИС УПК', 'time': '18:40', 'group': 2, 'online': False}], "Should be a list of dicts"


def test_make_phrase_not_have_lessons_today():
    with time_machine.travel(date(2022, 3, 8)):
        assert app.make_today_lessons_phrase().lstrip('Сегодня нет пар. ') in sayings.HARM_IDLENESS


def test_make_phrase_have_lessons_today():
    with time_machine.travel(date(2022, 2, 25)):
        assert app.make_today_lessons_phrase() == 'Сегодня у вас: ФМ и ИА, АБД, ИС УПК, РИКТ и ОП, ИС УПК'


def test_make_phrase_not_have_lessons_tomorrow():
    with time_machine.travel(date(2022, 3, 14)):
        assert app.make_tomorrow_lessons_phrase().lstrip('Завтра нет пар. ') in sayings.HARM_IDLENESS


def test_make_phrase_have_lessons_tomorrow():
    with time_machine.travel(date(2022, 3, 16)):
        assert app.make_tomorrow_lessons_phrase() == 'Завтра у вас будет: Социология, Философия'


def test_is_query_for_tomorrow():
    with time_machine.travel(date(2022, 3, 14)):
        assert app.is_query_timetable_tomorrow('какие завтра пары') == True


def test_is_query_for_timetable():
    assert app.is_query_for_timetable('какие уроки сегодня') == True


def test_is_query_not_for_timetable():
    assert app.is_query_for_timetable('спасибо') == False


def test_make_monday_day_lessons_phrase():
    assert app.make_particular_day_lessons_phrase('какие уроки в понедельник') == \
           'В понедельник у вас: Логистика, ИТУ, БП, РИКТ и ОП'


def test_make_tuesday_day_lessons_phrase():
    assert app.make_particular_day_lessons_phrase('какие уроки во вторник').lstrip('В вторник пар нет. ') in sayings.HARM_IDLENESS




