import pytest
from app import app

test_data = {
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
        "command": "какие уроки сегодня",
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
}


@pytest.fixture()
def client():
    return app.test_client()


def test_main_app_today(client):
    response = client.post('/alice', json={
        "request": {
            "command": "какие уроки сегодня"
        }
    })
    assert "Сегодня нет пар" == response.json["response"]["text"]


def test_main_app_tomorrow(client):
    response = client.post('/alice', json={
        "request": {
            "command": "какие уроки сегодня"
        }
    })
    assert "Сегодня нет пар" == response.json["response"]["text"]