from datetime import date
import timetable
import app
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


def test_query_lessons_for_today():
    assert app.is_query_timetable_today('какие сегодня уроки') == True


def test_query_lessons_for_not_today():
    assert app.is_query_timetable_today('какие завтра пары') == False


def test_make_phrase_not_have_lessons_today():
    with time_machine.travel(date(2022, 3, 8)):
        assert app.make_today_lessons_phrase() == 'Сегодня нет пар', "Should be phrase 'no lessons today' "


def test_make_phrase_have_lessons_today():
    with time_machine.travel(date(2022, 2, 25)):
        assert app.make_today_lessons_phrase() == 'Сегодня у вас: ФМ и ИА, АБД, ИС УПК, РИКТ и ОП, ИС УПК'






