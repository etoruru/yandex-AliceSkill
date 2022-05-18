import datetime
import json

import os


if os.environ["PYTEST_CURRENT_TEST"]:
    DATA_FILE = "timetable-sample.json"
else:
    DATA_FILE = "timetable.json"

DAYS = {
    'понедельник': 'Monday',
    'вторник': 'Tuesday',
    'среда': 'Wednesday',
    'четверг': 'Thursday',
    'пятница': 'Friday',
    'суббота': 'Saturday',
}


def read():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save(timetable):
    with open(DATA_FILE, 'w') as f:
        json.dump(timetable, f, indent=4, ensure_ascii=False)


def get_week_type(date):
    """ counts type week """
    if isinstance(date, str):
        date = datetime.date.today()
    (_, num_week, _) = date.isocalendar()
    if num_week % 2 == 0:
        return 'even'
    else:
        return 'odd'


def get_day(date):
    if isinstance(date, str):
        return translate_day(date)
    else:
        return date.strftime("%A")


def translate_day(day):
    return DAYS.get(day)


def get_lessons_for_day(date):
    """ reads timetable for a certain day, return list of dicts, sorted by time; date-datetime """
    day = get_day(date)

    timetable = read()
    if timetable.get(day):
        week_type = get_week_type(date)
        current_timetable = []
        persistent_tt = timetable[day].get('persistent')
        period_tt = timetable[day].get(week_type)
        if persistent_tt:
            current_timetable.extend(persistent_tt)

        if period_tt:
            current_timetable.extend(period_tt)

        return current_timetable or None
    else:
        return None

