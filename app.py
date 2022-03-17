from flask import Flask, request, jsonify
from datetime import date
import datetime

import timetable


PHRASES_TODAY = {
    'cкажи расписание на сегодня',
    'какие уроки сегодня',
    'какие предметы сегодня',
    'что сегодня по расписанию',
    'какие сегодня уроки',
    'какие сегодня пары',
    'какие пары на сегодня',
}

PHRASES_TOMORROW = {
    'cкажи расписание на завтра',
    'какие уроки завтра',
    'какие предметы завтра',
    'что завтра по расписанию',
    'какие завтра уроки',
    'какие завтра пары',
    'какие пары на завтра',
}

DAYS = {
    'понедельник': 'Monday',
    'вторник': 'Tuesday',
    'среда': 'Wensday',
    'четверг': 'Thurday',
    'пятница': 'Friday',
    'суббота': 'Saturday',
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
    elif is_query_timetable_today(command):
        phrase = make_today_lessons_phrase()
    elif is_query_timetable_tomorrow(command):
        phrase = make_tomorrow_lessons_phrase()

    response = {'text': phrase, 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}


def is_query_timetable_today(phrase):
    return phrase.lower() in PHRASES_TODAY


def is_query_timetable_tomorrow(phrase):
    return phrase.lower() in PHRASES_TOMORROW


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
        return 'Завтра у вас: ' + ', '.join(name_lessons)
    else:
        return 'Завтра нет пар'
