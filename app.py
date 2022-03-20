from flask import Flask, request, jsonify
from datetime import date
import datetime

import timetable

TIMETABLE_FLAGS = {
    'расписание',
    'уроки',
    'пары',
}

TODAY = 'сегодня'
TOMORROW = 'завтра'
YESTERDAY = 'вчера'

DAYS = {
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
}

app = Flask(__name__)


@app.route('/alice', methods=['POST'])
def main():
    payload = request.get_json() or {}

    response = create_response(payload)

    return jsonify(response)


def create_response(payload):
    version = payload.get('version')
    session = payload.get('session')
    command = payload.get('request', {}).get('command')
    phrase = ''
    if not command:
        phrase = "Привет. Спроси у меня что-то."
    elif is_query_for_timetable(command):
        if is_query_timetable_today(command):
            phrase = make_today_lessons_phrase()
        elif is_query_timetable_tomorrow(command):
            phrase = make_tomorrow_lessons_phrase()
        elif is_query_for_particular_day(command):
            phrase = make_particular_day_lessons_phrase()
        else:
            phrase = make_yesterday_lessons_phrase()
    else:
        pass

    response = {'text': phrase, 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}


def is_query_for_timetable(phrase):
    if set(phrase.lower().split()) & TIMETABLE_FLAGS:
        return True
    else:
        return False


def is_query_timetable_today(phrase):
    if phrase.lower().find(TODAY) != -1:
        return True
    else:
        return False


def is_query_timetable_tomorrow(phrase):
    if phrase.lower().find(TOMORROW) != -1:
        return True
    else:
        return False


def is_query_for_particular_day(phrase):
    if set(phrase.lower().split()) & DAYS:
        return True
    else:
        return False


def make_today_lessons_phrase():
    lessons = timetable.get_lessons_for_day(date.today())
    name_lessons = []
    if lessons:
        for lesson in lessons:
            name_lessons.append(lesson.get('name'))
        return 'Сегодня у вас: ' + ', '.join(name_lessons)
    else:
        return 'Сегодня нет пар'


def make_tomorrow_lessons_phrase():
    tomorrow_date = date.today() + datetime.timedelta(days=1)
    lessons = timetable.get_lessons_for_day(tomorrow_date)
    name_lessons = []
    if lessons:
        for lesson in lessons:
            name_lessons.append(lesson.get('name'))
        return 'Завтра у вас будет: ' + ', '.join(name_lessons)
    else:
        return 'Завтра нет пар'


def make_yesterday_lessons_phrase():
    yesterday_date = date.today() - datetime.timedelta(days=1)
    lessons = timetable.get_lessons_for_day(yesterday_date)
    name_lessons = []
    if lessons:
        for lesson in lessons:
            name_lessons.append(lesson.get('name'))
        return 'Вчера у вас было: ' + ', '.join(name_lessons)
    else:
        return 'Вчера пар не было'


def make_particular_day_lessons_phrase():
    pass


if __name__ == '__main__':
    is_query_for_timetable('какие уроки сегодня')
