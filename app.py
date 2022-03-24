from flask import Flask, request, jsonify
from datetime import date
import datetime

import timetable

TIMETABLE_FLAGS = {
    'расписание',
    'уроки',
    'пары',
}

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
        if is_query_timetable_yesterday(command):
            phrase = make_yesterday_lessons_phrase()
        elif is_query_timetable_tomorrow(command):
            phrase = make_tomorrow_lessons_phrase()
        elif is_query_for_particular_day(command):
            phrase = make_particular_day_lessons_phrase()
        else:
            phrase = make_today_lessons_phrase()
    else:
        pass

    response = {'text': phrase, 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}


def is_query_for_timetable(phrase):
    lexems = phrase.lower().split()
    return bool(TIMETABLE_FLAGS.intersection(set(lexems)))


def is_query_timetable_yesterday(phrase):
    return phrase.lower().find(YESTERDAY) != -1


def is_query_timetable_tomorrow(phrase):
    return phrase.lower().find(TOMORROW) != -1


def is_query_for_particular_day(phrase):
    lexems = phrase.lower().split()
    return bool(DAYS.intersection(set(lexems)))


def get_lessons_list(lessons):
    return [lesson.get('name') for lesson in lessons]


def get_day_from_phrase(phrase):
    lexems = phrase.lower().split()
    if DAYS.intersection(set(lexems)):
        return list(DAYS.intersection(set(lexems)))[0]
    else:
        return 'запрос не содержит день'


def make_today_lessons_phrase():
    lessons = timetable.get_lessons_for_day(date.today())
    if lessons:
        name_lessons = get_lessons_list(lessons)
        return 'Сегодня у вас: ' + ', '.join(name_lessons)
    else:
        return 'Сегодня нет пар. '


def make_tomorrow_lessons_phrase():
    tomorrow_date = date.today() + datetime.timedelta(days=1)
    lessons = timetable.get_lessons_for_day(tomorrow_date)
    if lessons:
        name_lessons = get_lessons_list(lessons)
        return 'Завтра у вас будет: ' + ', '.join(name_lessons)
    else:
        return 'Завтра нет пар. '


def make_yesterday_lessons_phrase():
    yesterday_date = date.today() - datetime.timedelta(days=1)
    lessons = timetable.get_lessons_for_day(yesterday_date)
    if lessons:
        name_lessons = get_lessons_list(lessons)
        return 'Вчера у вас было: ' + ', '.join(name_lessons)
    else:
        return 'Вчера пар не было. '


def make_particular_day_lessons_phrase(command):
    day = get_day_from_phrase(command)
    lessons = timetable.get_lessons_for_day(day)
    if lessons:
        name_lessons = get_lessons_list(lessons)
        return 'В {} у вас: '.format(day) + ', '.join(name_lessons)
    else:
        return 'В {} пар нет. '.format(day)




