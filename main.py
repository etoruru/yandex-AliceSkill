from flask import Flask, request, render_template, redirect, url_for
import json
import user_actions


app = Flask(__name__)

# for testing

@app.route('/', methods=['POST', 'GET'])
def get():
    if request.method == "POST":
        quest= request.form["nm"]
        return redirect(url_for("answer", question=quest))
    else:
        return render_template("index.html")

@app.route('/<question>')
def answer(question):
    return f'<h3>{make_answer(question)}</h3>'
    #return f'<h3>{make_answer(question)}</h3>'


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

if __name__ == '__main__':
    print(make_answer("'как зовут декана'"))