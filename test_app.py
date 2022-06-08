import json
from datetime import date
import os

import pytest
import time_machine

import app
import sayings
import timetable
import admin_commands
import constants


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
        assert app.is_query_timetable_tomorrow('какие завтра пары') is True


def test_is_query_for_timetable():
    assert app.is_query_for_timetable('какие уроки сегодня') is True


def test_is_query_not_for_timetable():
    assert app.is_query_for_timetable('спасибо') is False


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


# ------------------ TESTS FOR ADDING A NEW TIMETABLE--------------------------
@pytest.fixture(autouse=True)
def prepare_timetable():
    timetbl = timetable.read()
    with open('timetable-sample.json', 'w') as f:
        json.dump(timetbl, f, indent=4, ensure_ascii=False)


def test_make_lessons_order_list():
    assert admin_commands.make_lessons_order_list("первая пара математика, второй предмет бухучет у первой группы по числителю, четвертая информатика") == \
           [('первая', 'математика'), ('второй', 'бухучет'),  ('четвертая', 'информатика') ]


def test_lessons_time():
    assert admin_commands.lessons_time([('первая', 'математика'), ('второй', 'бухучет'), ('четвертая', 'информатика')]) ==\
           {'8:00': 'математика', '9:45': 'бухучет', '13:25': 'информатика'}


def test_lessons_time1():
    assert admin_commands.lessons_time([('первая', 'математика'), ('второй', 'бухучет'), ('шестой', 'АБД')]) ==\
           {'8:00': 'математика', '9:45': 'бухучет', '16:55': 'АБД'}


def test_all_lessons_time():
    assert admin_commands.lessons_time([('первая', 'математика'), ('второй', 'бухучет'), ('третья', 'информатика'),
                                        ('шестой', 'АБД'), ('пятая', 'физра'), ('четвертая', 'история'), ('седьмой', 'ИТУ')]) ==\
           {'8:00': 'математика', '9:45': 'бухучет', '11:30': 'информатика', '16:55': 'АБД', '15:10': 'физра', '13:25': 'история', '18:40': 'ИТУ'}


def test_is_add_command():
    assert app.is_command_add('Алиса, запиши расписание') is True


def test_valid_phrase1():
    assert admin_commands.is_valid('Алиса запиши расписание на понедельник,'
                                   ' информатика, математика, история') is False


def test_valid_phrase2():
    assert admin_commands.is_valid('Алиса добавь расписание, первая пара философия,'
                                   ' вторая методы исследования операций') is False


def test_create_new_timetable():
    if os.environ.get("PYTEST_CURRENT_TEST"):
        timetable.DATA_FILE = "timetable-sample.json"
    else:
        timetable.DATA_FILE = "timetable.json"
    assert admin_commands.add('Алиса, запиши расписание на понедельник первая пара информатика по числителю,'
                               ' второй предмет бухучет у второй группы, четвертая математика у первой группы') == constants.SUCCESS


def test_create_new_timetable1():
    assert admin_commands.add('Алиса, запиши расписание на среду первая пара БЖД по знаменателю, вторая пара БЖД по числителю, пятая пара игровые модели в электронном бизнесе,'
                              'шестая пара игровые модели в электронном бизнесе, седьмая пара игровые модели в электронном бизнесе по числителю') == constants.SUCCESS


def test_wrong_command_create():
    assert admin_commands.add('Алиса запиши расписание первая пара информатика, затем история у первой группы, затем математика') == constants.INCORRECT_COMMAND


def test_file():
    assert timetable.DATA_FILE == 'timetable-sample.json'


def test_is_command_add_help():
    assert app.is_command_adding_help('Алиса, дай справку: добавить расписание') is True


def test_is_command_help():
    assert app.is_command_help('Алиса, дай справку добавить расписание') is True


def test_is_command_help1():
    assert app.is_command_help('Алиса, что ты умеешь') is True


def test_is_add_command1():
    assert app.is_command_add('Алиса, дай справку добавить расписание') is True


def test_is_query_for_week_type():
    assert app.is_query_for_week_type('Алиса, какая сегодня неделя') is True


def test_is_query_for_week_type1():
    assert app.is_query_for_week_type('Алиса, сегодня числитель или знаменатель') is True


def test_is_query_for_week_type2():
    assert app.is_query_for_week_type('Алиса, сегодня числитель') is True


def test_is_query_for_week_type3():
    assert app.is_query_for_week_type('Алиса, какая неделя') is True


def test_answer_type():
    with time_machine.travel(date(2022, 3, 15)):
        assert app.answer_week_type("Алиса, сегодня знаменатель") == 'Нет, сейчас числитель'


def test_answer_type1():
    with time_machine.travel(date(2022, 3, 22)):
        assert app.answer_week_type("Алиса, сейчас знаменатель") == 'Да, сейчас знаменатель'


def test_is_delete_command():
    assert app.is_delete_command('Алиса, удали расписание на понедельник') == True


# def test_delete():
#     assert app.delete_timetable('Алиса, удали расписание на понедельник') == constants.SUCCESS_DELETE
#
#
# def test_day():
#     assert admin_commands.get_day('Алиса, удали расписание на понедельник') == ('понедельник', "понедельник")
#
# def test_delete_day():
#     assert admin_commands.delete_day('Алиса, удали расписание на понедельник') == constants.SUCCESS_DELETE
#
#
# def test_delete_day1():
#     assert admin_commands.delete_day('Алиса, сбрось расписание на вторник') == constants.FAIL_DELETE
#
#
# def test_delete_all():
#     assert admin_commands.delete_all() == constants.SUCCESS_DELETE


def test_is_query_tm_day():
    assert app.is_query_for_particular_day('Алиса, скажи расписание на понедельник') == True