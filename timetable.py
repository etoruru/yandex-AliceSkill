from datetime import date
import json


DATA_FILE = "timetable.json"


def read():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save(timetable):
    with open(DATA_FILE, 'w') as f:
        json.dump(timetable, f, indent=4, ensure_ascii=False)


def get_day_type(date):
    """ counts type week """
    (_, num_week, _) = date.isocalendar()
    if num_week % 2 == 0:
        return 'even'
    else:
        return 'odd'


def get_lessons_for_day(date):
    """ reads timetable for a certain day, return list of dicts, sorted by time; date-datetime """
    day = date.strftime("%A")

    timetable = read()

    if timetable.get(day):
        week_type = get_day_type(date)
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




