from flask import Flask, request, render_template
import json
import user_actions


app = Flask(__name__)

# for testing

@app.route('/')
def get():
    #return '<h1>Hello</h1>'
    return render_template('index.html')


# @app.route('/', methods=['POST'])
# def main():
#     request_data = request.get_json()
#
#     response = create_response(request_data)
#
#     return json.dumps(response, indent=4)




def create_response(request):
    version = request['version']
    session = request['session']
    content = request['request']['command']
    if not content:
        content = "Привет. Спроси у меня что-то."
    response = {'text': make_answer(content), 'end_session': 'false'}
    return {'version': version, 'session': session, 'response': response}


def make_answer(content):
    return user_actions.make_answer(content)

