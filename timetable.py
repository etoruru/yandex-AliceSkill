import json


DATA_FILE = "timetable.json"


def read():
    return json.load(DATA_FILE)


def save(timetable):
    json.dump(timetable, DATA_FILE, indent=4, ensure_ascii=False)





