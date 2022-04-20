import app
import sayings
import timetable

from datetime import date

import time_machine


def test_not_get_lessons():
    assert timetable.get_lessons_for_day(date(2022, 2, 22)) is None, "Should be None"


def test_get_lessons():
    assert timetable.get_lessons_for_day(date(2022, 2, 25)) == \
           [{'name': 'Финансовая математика и инвестиционный анализ', 'time': '9:45', 'group': None, 'online': False},
            {'name': 'Автоматизация бухгалтерской деятельности', 'time': '13:25', 'group': None, 'online': False},
            {'name': 'Информационные системы управления производственной компанией', 'time': '15:10', 'group': None, 'online': False},
            {'name': 'Рынки информационно-коммуникационных технологий и организация продаж', 'time': '16:55', 'group': None, 'online': False},
            {'name': 'Информационные системы управления производственной компанией', 'time': '18:40', 'group': 2, 'online': False}]


def test_make_phrase_not_have_lessons_today():
    with time_machine.travel(date(2022, 3, 8)):
        assert app.make_today_lessons_phrase().lstrip('Сегодня нет пар, но помните: ') \
               in sayings.HARM_IDLENESS


def test_make_phrase_have_lessons_today():
    with time_machine.travel(date(2022, 2, 25)):
        assert app.make_today_lessons_phrase() == \
               'Сегодня у вас: Финансовая математика и инвестиционный анализ, Автоматизация бухгалтерской деятельности,' \
               ' Информационные системы управления производственной компанией, Рынки информационно-коммуникационных технологий и организация продаж' \
               ' и Информационные системы управления производственной компанией у второй группы'


def test_make_phrase_not_have_lessons_tomorrow():
    with time_machine.travel(date(2022, 3, 14)):
        assert app.make_tomorrow_lessons_phrase().lstrip('Завтра нет пар, но помните: ') \
               in sayings.HARM_IDLENESS


def test_make_phrase_have_lessons_tomorrow():
    with time_machine.travel(date(2022, 3, 16)):
        assert app.make_tomorrow_lessons_phrase() == 'Завтра у вас будет: Социология и Философия'


def test_is_query_for_tomorrow():
    with time_machine.travel(date(2022, 3, 14)):
        assert app.is_query_timetable_tomorrow('какие завтра пары') == True


def test_is_query_for_timetable():
    assert app.is_query_for_timetable('какие уроки сегодня') == True


def test_is_query_not_for_timetable():
    assert app.is_query_for_timetable('спасибо') == False


def test_make_monday_day_lessons_phrase():
    with time_machine.travel(date(2022, 3, 14)):
        assert app.make_particular_day_lessons_phrase('какие уроки в понедельник') == \
               'В понедельник у вас: две пары по предмету: Логистика, Информационные технологии управления и Бизнес планирование'


def test_make_wensday_day_lessons_phrase():
    with time_machine.travel(date(2022, 3, 16)):
        assert app.make_particular_day_lessons_phrase('какие пары в среду') == \
               'В среду у вас: две пары по предмету: Управление ИТ-сервисами и контентом ' \
               'и Оценка и управление финансовыми рисками'


def test_make_friday_day_lessons_phrase():
    with time_machine.travel(date(2022, 3, 18)):
        assert app.make_particular_day_lessons_phrase('какие пары в пятницу') == \
               'В пятницу у вас: Финансовая математика и инвестиционный анализ, две пары по предмету: Автоматизация бухгалтерской деятельности, ' \
               'Информационные системы управления производственной компанией и ' \
               'Информационные системы управления производственной компанией у первой группы'


def test_make_tuesday_day_lessons_phrase():
    assert app.make_particular_day_lessons_phrase('какие уроки во вторник').lstrip('Во вторник пар нет, но помните: ') \
           in sayings.HARM_IDLENESS


def test_tomorrow():
    with time_machine.travel(date(2022, 3, 15)):
        assert app.make_tomorrow_lessons_phrase() == \
               'Завтра у вас будет: две пары по предмету: Управление ИТ-сервисами и контентом и ' \
               'Оценка и управление финансовыми рисками'
