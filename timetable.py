from datetime import datetime
import json


DATA_FILE = "timetable.json"


def read():
    return json.load(DATA_FILE)


def save(timetable):
    json.dump(timetable, DATA_FILE, indent=4, ensure_ascii=False)


def get_day_type(date):
    """ counts type week """
    (_, num_week, _) = date.isocalendar()
    if num_week % 2 == 0:
        return 'even'
    else:
        return 'odd'


def get_timetable_for_day(date):
    """ reads timetable for a certain day, return list of dicts, sorted by time; day-str, date-datetime """
    day = date.strftime("%A")
    timetable = read()

    if timetable.get(day, None):
        week_type = get_day_type(date)
        current_timetable = []
        persistent_tt = timetable[day].get('persistent', None)
        period_tt = timetable[day].get(week_type, None)
        if persistent_tt:
            current_timetable.extend(persistent_tt)

        if period_tt:
            current_timetable.extend(period_tt)

        return current_timetable
    else:
        return None




