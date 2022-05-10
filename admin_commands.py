import re


from constants import TIME, DAYS, GROUPS, WEEK_TYPES
from constants import SUCCESS, INCORRECT_COMMAND
import timetable


def make_lessons_order_list(phrase):
    clean_phrase = re.sub(r'\sпара\s|\sпредмет\s|\sурок\s|\sу\s|второй\sгруппы|первой\sгруппы|по|числителю|знаменателю', '', phrase)
    phrase_without_spaces = re.sub(r'\s', '', clean_phrase)
    return re.findall(r'(перв[аяоеуюий]{2}|втор[аяоеуюий]{2}|треть[аяоеуюий]|четверт[аяоеуюий]{2}'
                      r'|пят[аяоеуюий]{2}|шест[аяоеуюий]{2}|седьм[аяоеуюий]{2})(\w+)', phrase_without_spaces)


def get_week_type(phrase):
    clean_phrase = re.sub(r'\sпара\s|\sпредмет\s|\sурок\s|\sу\s|второй\sгруппы|первой\sгруппы|'
                          r'перв[аяоеуюий]{2}|втор[аяоеуюий]{2}|треть[аяоеуюий]|четверт[аяоеуюий]{2}'
                          r'|пят[аяоеуюий]{2}|шест[аяоеуюий]{2}|седьм[аяоеуюий]{2}|по','', phrase)
    phrase_without_spaces = re.sub(r'\s', '', clean_phrase)
    return re.findall(r'(\w+)(числителю|знаменателю)', phrase_without_spaces)


def make_list_name_group(phrase):
    return re.findall(r'(\w+)(\sу\sвторой\sгруппы|\sу\sпервой\sгруппы)', phrase)


def make_cut_phrase(phrase, day):
    index = phrase.find(day)
    return phrase[index + len(day) + 1:]


def create_new_timetable(phrase):
    old_timetable = timetable.read()
    day = get_day(phrase)
    cut_phrase = make_cut_phrase(phrase, day)
    lessons_lst = make_lessons_list(cut_phrase)
    lessons_divided_weeks = divide_week_type(lessons_lst, cut_phrase)
    for week, lessons in lessons_divided_weeks.items():
        old_timetable[timetable.DAYS.get(day)][week].extend(lessons)
    return old_timetable


def what_week_type(name, phrase):
    lesson_week_type = get_week_type(phrase)
    if lesson_week_type:
        for lesson, week in lesson_week_type:
            if name == lesson:
                return WEEK_TYPES.get(week)
    else:
        return 'persistent'


def divide_week_type(lessons, phrase):
    persistent = []
    odd = []
    even = []
    for lesson in lessons:
        if what_week_type(lesson['name'], phrase) == 'even':
            even.append(lesson)
        elif what_week_type(lesson['name'], phrase) == 'odd':
            odd.append(lesson)
        else:
            persistent.append(lesson)
    return {'even': even, 'odd': odd, 'persistent': persistent}


def make_lessons_list(phrase):
    lessons_lst = []
    lessons_time_dict = lessons_time(phrase)
    group_list = make_list_name_group(phrase)
    for name, time in lessons_time_dict.items():
        lesson = make_dict(name, time)
        if group_list:
            for name_g, group_num in group_list:
                if name_g == name:
                    lesson['group'] = GROUPS.get(group_num.lstrip())
        lessons_lst.append(lesson)
    return lessons_lst


def make_dict(name, time, group=None, online=False):
    return {'name': name, 'time': time, 'group': group, 'online': online}


def define_time(lesson_num):
    for num, time in TIME.items():
        if num in lesson_num:
            return time


def lessons_time(phrase):
    lessons_time_dict = {}
    for num, name in make_lessons_order_list(phrase):
        lessons_time_dict[name] = define_time(num)
    return lessons_time_dict

phrase = 'Алиса, запиши расписание на понедельник первая пара информатика по числителю, второй предмет бухучет у второй группы, четвертая математика у первой группы'
#phrase = 'Алиса запиши расписание первая пара информатика, затем история'


def get_day(phrase):
    phrase_list = phrase.split()
    for word in phrase_list:
        if word in DAYS.keys():
            return DAYS.get(word)


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





