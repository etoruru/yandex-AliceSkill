from flask import Flask, request
import json


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
    response = {'text': content, 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}

