from flask import Flask, request
from datetime import date
import json
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

App = Flask(__name__)


@App.route('/alice', methods=['POST'])
def main():
    payload = request.get_json() or {}

    response = create_response(payload)

    return json.dumps(response, indent=4)


def create_response(payload):
    version = payload.get('version')
    session = payload.get('session')
    command = payload.get('request', {}).get('command')
    phrase = ''
    if not command:
        phrase = "Привет. Спроси у меня что-то."
    elif is_query_timetable_today(command):
        phrase = make_today_lessons_phrase()

    response = {'text': phrase, 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}


def is_query_timetable_today(phrase):
    return phrase.lower() in PHRASES_TODAY


def make_today_lessons_phrase():
    lessons = timetable.get_lessons_for_day(date.today())
    name_lessons = []
    if lessons:
        for lesson in lessons:
            name_lessons.append(lesson.get('name'))
        return 'Сегодня у вас: ' + ', '.join(name_lessons)
    else:
        return 'Сегодня нет пар'


if __name__ == '__main__':
    text = create_response({
        "session": {
            "message_id": 0,
            "session_id": "71c04dcc-fbb4-481b-b4a6-f4c7ead96f88",
            "skill_id": "640dc558-3fd2-431b-b76f-a001ad259435",
            "user": {
                "user_id": "C0765AA7B46D2628CC015BADB91FD164EC236E32122F641D3881797D7B96E0D2"
            },
            "application": {
                "application_id": "6C6F1A277DDD90A352D468D2327064D8CDF652B43F77E24351DABFB31BA89618"
            },
            "user_id": "6C6F1A277DDD90A352D468D2327064D8CDF652B43F77E24351DABFB31BA89618",
            "new": True
        },
        "request": {
            "command": "Привет. Как дела?",
            "original_utterance": "",
            "nlu": {
                "tokens": [],
                "entities": [],
                "intents": {}
            },
            "markup": {
                "dangerous_context": False
            },
            "type": "SimpleUtterance"
        },
        "version": "1.0"
    })
    print(text)



