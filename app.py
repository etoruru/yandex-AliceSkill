from flask import Flask, request, jsonify

from datetime import date
import datetime
import random
import collections
import re

from constants import DAYS, DAYS_RESPONSE
import constants
import sayings
import timetable
import admin_commands


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
    phrase = constants.HELP
    if not command:
        phrase = constants.GREETING
    elif is_command_adding_help(command):
        phrase = get_help_adding()
    elif is_command_add(command):
        phrase = add_new_timetable(command)
    elif is_delete_command(command):
        phrase = delete_timetable(command)
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
        elif is_command_help(command):
            phrase = get_help()
        elif is_query_for_week_type(command):
            phrase = answer_week_type(command)
    response = {'text': phrase, 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}


def is_query_for_timetable(phrase):
    lexems = phrase.lower().split()
    return bool(constants.TIMETABLE_FLAGS.intersection(set(lexems)))


def is_query_timetable_yesterday(phrase):
    return phrase.lower().find(constants.YESTERDAY) != -1


def is_query_timetable_tomorrow(phrase):
    return phrase.lower().find(constants.TOMORROW) != -1


def is_query_for_particular_day(phrase):
    lexems = phrase.lower().split()
    days_set = set(DAYS.keys())
    return bool(days_set.intersection(set(lexems)))


def is_command_thank(phrase):
    return phrase.lower().find(constants.THANK) != -1


def is_command_help(phrase):
    for elem in constants.ASK_HELP:
        if elem in phrase.lower():
            return True
    return False


def is_command_adding_help(phrase):
    return is_command_help(phrase) and is_command_add(phrase)


def is_command_add(phrase):
    lexems = phrase.lower().split()
    return bool(constants.ADD_COMMAND.intersection(set(lexems)))


def is_query_for_week_type(phrase):
    lexems = phrase.lower().split()
    return bool(constants.ASK_WEEK_TYPE.intersection(set(lexems)))


def is_delete_command(phrase):
    return bool(re.search(r'??????????[??????]+|????????[??????]+', phrase))


def count_same_lessons(lessons):
    amount_lessons = collections.OrderedDict()
    for lesson in lessons:
        count = amount_lessons.get(lesson, 0)
        amount_lessons[lesson] = count + 1
    return amount_lessons


def group_lessons(lessons):
    lessons_to_count = []
    for lesson in lessons:
        if lesson.get('group') == 1:
            name_lesson = lesson.get('name') + ' ?? ???????????? ????????????'
            lessons_to_count.append(name_lesson)
        elif lesson.get('group') == 2:
            name_lesson = lesson.get('name') + ' ?? ???????????? ????????????'
            lessons_to_count.append(name_lesson)
        else:
            lessons_to_count.append(lesson.get('name'))
    grouped_lessons = count_same_lessons(lessons_to_count)
    return grouped_lessons


def get_day_from_phrase(phrase):
    lexems = phrase.lower().split()
    days_set = set(DAYS.keys())
    day = list(days_set.intersection(set(lexems)))
    if day:
        return DAYS[day[0]]
    else:
        return '???????????? ???? ???????????????? ????????'


def post_idleness():
    return ', ???? ??????????????: ' + random.choice(sayings.HARM_IDLENESS)


def concatenate_with_and(lessons):
    lessons_lst = []
    for (lesson, count) in lessons.items():
        if count == 2:
            lessons_lst.append('?????? ???????? ???? ????????????????: ' + lesson)
        else:
            lessons_lst.append(lesson)
    return ', '.join(lessons_lst[:-1]) + ' ?? ' + lessons_lst[-1]


def post_thank_response():
    return ' ?? ??????????????: ' + random.choice(sayings.THANK_RESPONSE)


def make_today_lessons_phrase():
    lessons = timetable.get_lessons_for_day(date.today())
    if lessons:
        name_lessons = group_lessons(lessons)
        return '?????????????? ?? ??????: ' + concatenate_with_and(name_lessons)
    else:
        return '?????????????? ?????? ??????' + post_idleness()


def make_tomorrow_lessons_phrase():
    tomorrow_date = date.today() + datetime.timedelta(days=1)
    lessons = timetable.get_lessons_for_day(tomorrow_date)
    if lessons:
            name_lessons = group_lessons(lessons)
            return '???????????? ?? ?????? ??????????: ' + concatenate_with_and(name_lessons)
    else:
        return '???????????? ?????? ??????' + post_idleness()


def make_yesterday_lessons_phrase():
    yesterday_date = date.today() - datetime.timedelta(days=1)
    lessons = timetable.get_lessons_for_day(yesterday_date)
    if lessons:
        name_lessons = group_lessons(lessons)
        return '?????????? ?? ?????? ????????: ' + concatenate_with_and(name_lessons)
    else:
        return '?????????? ?????? ???? ????????.'


def make_particular_day_lessons_phrase(command):
    day = get_day_from_phrase(command)
    lessons = timetable.get_lessons_for_day(day)
    if lessons:
        name_lessons = group_lessons(lessons)
        return '{} ?? ??????: '.format(DAYS_RESPONSE.get(day)) + concatenate_with_and(name_lessons)
    else:
        return '{} ?????? ??????'.format(DAYS_RESPONSE.get(day)) + post_idleness()


def answer_for_thank():
    return '????????????????????' + post_thank_response()


def get_help():
    return constants.ABOUT


def get_help_adding():
    return constants.ADDING_ABOUT


def add_new_timetable(command):
    return admin_commands.add(command)


def answer_week_type(command):
    current_type = constants.WEEK_TYPES.get(timetable.get_week_type(date.today()))
    if re.fullmatch(r'(??????????, (??????????????|????????????) (??????????????????|??????????????????????))', command.lower()):
        if '??????????????????' in command.lower() and current_type == '??????????????????':
            return '????, ???????????? ' + current_type
        else:
            if '??????????????????????' in command.lower() and current_type == '??????????????????????':
                return '????, ???????????? ' + current_type
            else:
                return '??????, ???????????? ' + current_type
    return '?????????????? ' + current_type


def delete_timetable(command):
    return admin_commands.delete(command)



