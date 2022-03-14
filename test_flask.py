import pytest
from app import App


@pytest.fixture()
def app():
    app=App
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_main_app(client):
    response = client.post('/alice', json={
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
    assert response.json.get('request').get('command') == 'Привет. Как дела?'
