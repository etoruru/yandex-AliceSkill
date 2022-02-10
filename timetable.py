import json
from datetime import datetime


DATA_FILE = "timetable.json"


def what_period_():
    """ counts type week """
    year, num_week, num_day = datetime.now().isocalendar()
    if num_week % 2 == 0:
        return 'even'
    else:
        return 'odd'


def get_period(period):
    period_dict = {'знаменатель': 'even', 'числитель': 'odd'}
    if period in period_dict:
        return period_dict[period]
    else:
        return 'persistent'



def get_day(day):
    """ translates  days of week in russian into english """
    days_dict = {'Понедельник': 'Monday', 'Вторник': 'Tuesday', 'Среда': 'Wensday', 'Четверг': 'Thursday', 'Пятиница': 'Friday', 'Суббота': 'Saturday'}
    if day in days_dict:
        return days_dict[day]
    else:
        raise KeyError


with open(DATA_FILE, "r") as f:
    timetable = json.load(f)




def create_subjects_names_lst(schedule):
    names = []
    for subject in schedule:
        names.append(subject.get('name'))
    return names


def read():
    """ reads timetable for a certain day, return list of dicts, sorted by time """
    day = get_day('Понедельник')

    if timetable.get(day, None):
        current_timetable = timetable[day].get('persistent', None)
        period_tt = timetable[day].get(what_period_(), None)
        if period_tt:
            current_timetable.extend(period_tt)
        current_timetable.sort(key=lambda subject: subject['time'])
        return current_timetable
    else:
        return 'No lessons!'


def save(data):
    day = get_day(data['day'])
    name = data['name']
    group = data['group']
    time = data['time']
    online = data['online']
    period = get_period(data['period'])
    subject_keys = ['name', 'time', 'group', 'online']
    subject = dict(zip(subject_keys, [name, time, group, online]))

    timetable[day][period].append(subject)




if __name__ == '__main__':
    read()





