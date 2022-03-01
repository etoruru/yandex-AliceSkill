from flask import Flask, request
from datetime import date
import json
import timetable



app = Flask(__name__)


@app.route('/alice', methods=['POST'])
def main():
    request_data = request.get_json()

    response = create_response(request_data)

    return json.dumps(response, indent=4)


def create_response(request):
    version = request['version']
    session = request['session']
    content = request['request']['command']
    if not content:
        content = "Привет. Спроси у меня что-то."
    elif is_query_timetable_today(content):
        content = make_today_lessons_phrase()

    response = {'text': content, 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}


def is_query_timetable_today(phrase):
    query_phrases_today = ['cкажи расписание на сегодня', 'какие уроки сегодня', 'какие предметы сегодня',
                           'что сегодня по расписанию', 'какие сегодня уроки']
    return True if phrase.lower() in query_phrases_today else False


def make_today_lessons_phrase():
    lessons = timetable.get_lessons_for_day(date.today())
    name_lessons = []
    if lessons:
        for lesson in lessons:
            name_lessons.append(lesson.get('name'))
        return 'Сегодня у вас: ' + ', '.join(name_lessons)
    else:
        return 'Сегодня нет пар'







