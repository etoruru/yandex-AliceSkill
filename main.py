from flask import Flask, request
import json


app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return '<h2>Hello world</h2>'

@app.route('/json', methods=['POST'])
def index():
    request_data = request.get_json()

    version = request_data['version']
    session = request_data['session']
    content = request_data['request']['command']
    response = {'text': "Hello! I'll repeat anything you say to me."}

    response_dict = {'version': version, 'session': session, 'response': response}
    json_obj = json.dumps(response_dict, indent=4)
    return json_obj