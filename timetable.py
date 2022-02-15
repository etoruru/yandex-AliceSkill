from datetime import datetime
import json


DATA_FILE = "timetable.json"


def read(f):
    # функция load требует объект union или объект, который возращает контекстный менеджер
    return json.load(f)


def save(timetable, fle):
    json.dump(timetable, fle, indent=4, ensure_ascii=False)


def what_period_(num_week):
    """ counts type week """
    if num_week % 2 == 0:
        return 'even'
    else:
        return 'odd'


def get_timetable_for_day(day, date):
    """ reads timetable for a certain day, return list of dicts, sorted by time; day-str, date-datetime """

    timetable = read() # вот здесь вопрос, где надо читать файл и где надо загружать его.
    # Если в этой функции, то нужно будет передвать объект контекстного менеждера. Не понимаю как это должно работать.

    year, num_week, num_day = date.isocalendar()
    if timetable.get(day, None):
        current_timetable = []
        persistent_tt = timetable[day].get('persistent', None)
        period_tt = timetable[day].get(what_period_(num_week), None)
        if persistent_tt:
            current_timetable.extend(persistent_tt)

        if period_tt:
            current_timetable.extend(period_tt)

        return current_timetable
    else:
        return 'No lessons!'


if __name__ == '__main__':
    with open(DATA_FILE, 'r') as f:
        print(type(f))

