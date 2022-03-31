from flask import Flask, request, jsonify
from datetime import date
import datetime
import random

import sayings
import timetable

TIMETABLE_FLAGS = {
    'расписание',
    'уроки',
    'пары',
}

TOMORROW = 'завтра'
YESTERDAY = 'вчера'

THANK = 'спасибо'

DAYS = {
    'понедельник': 'понедельник',

    'вторник': 'вторник',

    'среду': 'среда',
    'средам': 'среда',
    'среде': 'среда',

    'четвергу': 'четверг',
    'четверг': 'четверг',

    'пятницу': 'пятница',
    'пятнице': 'пятница',

    'субботу': 'суббота',
    'субботе': 'суббота',

    'воскресенье': 'воскресенье',
}

DAYS_RESPONSE = {
    'понедельник': 'В понедельник',
    'вторник': 'Во вторник',
    'среда': 'В среду',
    'четверг': 'В четверг',
    'пятница': 'В пятницу',
    'суббота': 'В субботу',
    'воскресенье': 'В воскресенье',
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
            phrase = make_particular_day_lessons_phrase(command)
        else:
            phrase = make_today_lessons_phrase()
    else:
        if is_command_thank(command):
            phrase = answer_for_thank()

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
    days_set = set(DAYS.keys())
    return bool(days_set.intersection(set(lexems)))


def is_command_thank(phrase):
    return phrase.lower().find(THANK) != -1


def get_lessons_list(lessons):
    lessons_list = []
    for lesson in lessons:
        if lesson.get('group') == 1:
            name_lesson = lesson.get('name') + ' у первой группы'
            lessons_list.append(name_lesson)
        elif lesson.get('group') == 2:
            name_lesson = lesson.get('name') + ' у второй группы'
            lessons_list.append(name_lesson)
        else:
            lessons_list.append(lesson.get('name'))

    return lessons_list


def get_day_from_phrase(phrase):
    lexems = phrase.lower().split()
    days_set = set(DAYS.keys())
    day = list(days_set.intersection(set(lexems)))
    if day:
        return DAYS[day[0]]
    else:
        return 'запрос не содержит день'


def post_idleness():
    return ', но помните: ' + random.choice(sayings.HARM_IDLENESS)


def concatenate_with_and(lessons):
    return ', '.join(lessons[:-1]) + ' и ' + lessons[-1]


def post_thank_response():
    return ' и помните: ' + random.choice(sayings.THANK_RESPONSE)


def make_today_lessons_phrase():
    lessons = timetable.get_lessons_for_day(date.today())
    if lessons:
        name_lessons = get_lessons_list(lessons)
        return 'Сегодня у вас: ' + concatenate_with_and(name_lessons)
    else:
        return 'Сегодня нет пар' + post_idleness()


def make_tomorrow_lessons_phrase():
    tomorrow_date = date.today() + datetime.timedelta(days=1)
    lessons = timetable.get_lessons_for_day(tomorrow_date)
    if lessons:
            name_lessons = get_lessons_list(lessons)
            return 'Завтра у вас будет: ' + concatenate_with_and(name_lessons)
    else:
        return 'Завтра нет пар' + post_idleness()


def make_yesterday_lessons_phrase():
    yesterday_date = date.today() - datetime.timedelta(days=1)
    lessons = timetable.get_lessons_for_day(yesterday_date)
    if lessons:
        name_lessons = get_lessons_list(lessons)
        return 'Вчера у вас было: ' + concatenate_with_and(name_lessons)
    else:
        return 'Вчера пар не было.'


def make_particular_day_lessons_phrase(command):
    day = get_day_from_phrase(command)
    lessons = timetable.get_lessons_for_day(day)
    if lessons:
        name_lessons = get_lessons_list(lessons)
        return '{} у вас: '.format(DAYS_RESPONSE.get(day)) + concatenate_with_and(name_lessons)
    else:
        return '{} пар нет'.format(DAYS_RESPONSE.get(day)) + post_idleness()


def answer_for_thank():
    return 'Пожалуйста' + post_thank_response()

