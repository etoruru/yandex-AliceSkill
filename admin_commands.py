import re

from constants import TIME, DAYS, GROUPS, WEEK_TYPES
from constants import SUCCESS, INCORRECT_COMMAND
import timetable
import constants


def make_correct_lessons_name(phrase):
    clean_phrase = re.sub(r'пара|предмет|урок|\sу\s|второй\sгруппы|первой\sгруппы|по|числителю|знаменателю|'
                          r'перв[аяоеуюий]{2}|втор[аяоеуюий]{2}|треть[аяоеуюий]|четверт[аяоеуюий]{2}'
                          r'|пят[аяоеуюий]{2}|шест[аяоеуюий]{2}|седьм[аяоеуюий]{2}', '', phrase)
    names = [elem.strip(' ') for elem in clean_phrase.split(',')]
    unique_lessons = set(list(filter(None, names)))
    return unique_lessons


def add_spaces(lesson, correct_names):
    for name in correct_names:
        if lesson == name.replace(' ', ''):
            return name


def make_lessons_order_list(phrase):
    clean_phrase = re.sub(r'\sпара\s|\sпредмет\s|\sурок\s|\sу\s|второй\sгруппы|'
                          r'первой\sгруппы|по|числителю|знаменателю','', phrase)
    phrase_without_spaces = re.sub(r'\s', '', clean_phrase)
    return re.findall(r'(перв[аяоеуюий]{2}|втор[аяоеуюий]{2}|треть[аяоеуюий]|четверт[аяоеуюий]{2}'
                      r'|пят[аяоеуюий]{2}|шест[аяоеуюий]{2}|седьм[аяоеуюий]{2})(\w+)', phrase_without_spaces)


def get_week_type(phrase):
    clean_phrase = re.sub(r'\sпара\s|\sпредмет\s|\sурок\s|\sу\s|второй\sгруппы|первой\sгруппы|'
                          r'по','', phrase)
    phrase_without_spaces = re.sub(r'\s', '', clean_phrase)
    return re.findall(r'(перв[аяоеуюий]{2}|втор[аяоеуюий]{2}|треть[аяоеуюий]|четверт[аяоеуюий]{2}'
                      r'|пят[аяоеуюий]{2}|шест[аяоеуюий]{2}|седьм[аяоеуюий]{2})'
                      r'(\w+)(числителю|знаменателю)', phrase_without_spaces)


def make_list_name_group(phrase):
    return re.findall(r'(\w+)(\sу\sвторой\sгруппы|\sу\sпервой\sгруппы)', phrase)


def make_cut_phrase(phrase, day):
    index = phrase.find(day)
    return phrase[index + len(day) + 1:]


def create_new_timetable(phrase):
    old_timetable = timetable.read()
    day, day_original = get_day(phrase)
    day_eng = timetable.DAYS.get(day)
    cut_phrase = make_cut_phrase(phrase, day_original)
    time = make_lessons_order_list(cut_phrase)
    groups = make_list_name_group(cut_phrase)
    weeks = get_week_type(cut_phrase)
    correct_names = make_correct_lessons_name(cut_phrase)
    lessons_lst = make_lessons_list(time, groups)
    lessons_divided_weeks = divide_week_type(lessons_lst, weeks, correct_names)

    if old_timetable.get(day_eng):
        for week, lessons in lessons_divided_weeks.items():
            old_timetable[day_eng][week].extend(lessons)
    else:
        old_timetable[day_eng] = lessons_divided_weeks
    return old_timetable


def what_week_type(name, time, lesson_week_type):
    if lesson_week_type:
        for time_word, lesson, week in lesson_week_type:
            if name == lesson and time == define_time(time_word):
                return WEEK_TYPES.get(week)
    else:
        return 'persistent'


def divide_week_type(lessons, weeks, correct_names):
    persistent = []
    odd = []
    even = []
    for lesson in lessons:
        if what_week_type(lesson['name'], lesson['time'], weeks) == 'even':
            lesson['name'] = add_spaces(lesson['name'], correct_names)
            even.append(lesson)
        elif what_week_type(lesson['name'], lesson['time'], weeks) == 'odd':
            lesson['name'] = add_spaces(lesson['name'], correct_names)
            odd.append(lesson)
        else:
            lesson['name'] = add_spaces(lesson['name'], correct_names)
            persistent.append(lesson)
    return {'even': even, 'odd': odd, 'persistent': persistent}


def make_lessons_list(time, group_list):
    lessons_lst = []
    lessons_time_dict = lessons_time(time)
    for time, name in lessons_time_dict.items():
        lesson = make_lesson(name, time)
        if group_list:
            for name_g, group_num in group_list:
                if name_g == name:
                    lesson['group'] = GROUPS.get(group_num.lstrip())
        lessons_lst.append(lesson)
    return lessons_lst


def make_lesson(name, time, group=None, online=False):
    return {'name': name, 'time': time, 'group': group, 'online': online}


def define_time(lesson_num):
    for num, time in TIME.items():
        if num in lesson_num:
            return time


def lessons_time(time):
    lessons_time_dict = {}
    for num, name in time:
        lessons_time_dict[define_time(num)] = name
    return lessons_time_dict


def get_day(phrase):
    phrase_list = phrase.split()
    for word in phrase_list:
        if word in DAYS.keys():
            return (DAYS.get(word), word)


def is_valid(phrase):
    clean_phrase = re.sub(r'пара|предмет|урок|\sу\s|второй\sгруппы|первой\sгруппы|\sпо\s|числителю|знаменателю', '', phrase)
    match_day = re.search(r'(понедельник|вторник|среду|четверг|пятницу|субботу|воскресенье)', clean_phrase)
    match_order = re.findall(r'(перв[аяоеуюий]{2}|втор[аяоеуюий]{2}|трет[ьаяоеуюий]{2}|четверт[аяоеуюий]{2}'
                             r'|пят[аяоеуюий]{2}|шест[аяоеуюий]{2}|седьм[аяоеуюий]{2})', clean_phrase)
    match_block_words = re.findall(r'(затем|потом|далее)', clean_phrase)
    if match_day and match_order and not match_block_words:
        return True
    else:
        return False


def add(command):
    if is_valid(command):
        new_timetable = create_new_timetable(command)
        timetable.save(new_timetable)
        return SUCCESS
    else:
        return INCORRECT_COMMAND


def is_command_delete_day(command):
    return bool(re.search(r'понедельник|вторнк|среду|четверг|пятницу|субботу|воскресенье', command))


def delete_all():
    timetable.save({})
    return constants.SUCCESS_DELETE


def delete_day(command):
    day, _ = get_day(command)
    day_eng = timetable.DAYS.get(day)
    old_timetable = timetable.read()
    if old_timetable.get(day_eng):
        del old_timetable[day_eng]
        timetable.save(old_timetable)
        return constants.SUCCESS_DELETE
    else:
        return constants.FAIL_DELETE


def delete(command):
    if is_command_delete_day(command):
        return delete_day(command)
    else:
        return delete_all()

