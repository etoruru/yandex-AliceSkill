from flask import Flask, request
import json


app = Flask(__name__)

# for testing
# @app.route('/', methods=['GET'])
# def get():
#     return '<h2>Hello world</h2>'

@app.route('/', methods=['POST'])
def main():
    request_data = request.get_json()

    response = create_response(request_data)

    return json.dumps(response, indent=4)

def create_response(request):
    version = request['version']
    session = request['session']
    content = request['request']['command']
    if not content:
        content = "Hello! I'll repeat anything you say to me."
    response = {'text': content, 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}

