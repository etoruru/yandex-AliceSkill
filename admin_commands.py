import re


TIME = {
    'перв': '8:00',
    'втор': '9:45',
    'трет': '11:30',
    'четверт': '13:25',
    'пят': '15:10',
    'шест': '16:55',
    'седьм': '18:40',
}

phrase1 = "первая пара математика, второй предмет бухучет, четвертая информатика"


def make_lessons_order_list(phrase):
    clean_phrase = re.sub(r'пара|урок|предмет|\s', '', phrase)
    return re.findall(r'(перв[аяоеуюий]{2}|втор[аяоеуюий]{2}|трет[аяоеуюий]{2}|четверт[аяоеуюий]{2}'
                      r'|пят[аяоеуюий]{2}|шест[аяоеуюий]{2}|седьм[аяоеуюий]{2})(\w+)', clean_phrase)


def define_time(lesson_num):
    for num, time in TIME.items():
        if num in lesson_num:
            return time


def lessons_time(lessons_order_list):
    lessons_time_dict = {}
    for num, name in lessons_order_list:
        lessons_time_dict[name] = define_time(num)
    return lessons_time_dict








