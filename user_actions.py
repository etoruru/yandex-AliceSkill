import database


alice_phrases = {'ask_continue': ["Хотите продолжить?", "Продолжим?", "Продолжаем?", "Хотите еще что-то узнать?", "Хотите еще спросить?"],
                 'fallback_general': ['Прости, я, наверное, тебя не расслышала. Повтори, пожалуйста.', 'Моя нейросеть не смогла идентифицировать твой ответ. Попробуй повторить',
                                      'Не могу расшифровать твой ответ, можешь перефразировать?'],
                 'fallback_question': ['Моя нейросеть не смогла идентифицировать твой ответ. Вы можете спросить: '],
                 'greeting': ['Добро пожаловать на факультет ПММ. Если у вас есть вопросы, о факультете, я постараюсь помочь вам.',
                              'Добро пожаловать, на факультет Прикладной математики, информатики и механики. Что вы хотите узнать?'] }


def show_questions():
    pass


user_phrases = {'confirm': ["да", "конечно", "хорошо", "давай", "да конечно", "конечно да", "да давай", "ага", "да да"],
                'continue': ['давай продолжим', 'продолжим', 'продолжаем', 'хочу продолжить', 'давай продолжать',
                             'продолжай', 'давай продолжай', 'продолжи', 'продолжить', 'продолжать'],
                'repeat': ['повтори', 'ещё раз', 'еще раз', 'скажи ещё раз', 'давай ещё раз', 'повторить', 'можешь повторить', 'повтори вопрос'],
                'repeat_options': ['повтори варианты', 'пожалуйста повтори варианты', 'какие варианты', 'какие варианты вопросов',
                                   'варианты вопросов', 'повтори пожалуйста варианты','повтори пожалуйста варианты вопросов', 'какие есть варианты'],
                'deny': ['нет', 'не хочу', 'не надо', 'не думаю', 'наверное нет', 'конечно нет', 'не надо', 'нет нет']}




def clear_text(command):
    pass


def define_phrase_type(command, phrases):
    type_phrase = 'question'
    answer = clear_text(command)
    for key in phrases:
        if answer in phrases[key]:
            type_phrase = key
    return type_phrase


def confirm():
    pass


def do_continue():
    pass


def repeat():
    pass


def repeat_options():
    pass


def deny():
    pass


def answer(command):
    return database.find_answer(command)


def make_answer(command):
    type_phrase = define_phrase_type(command, user_phrases)
    if type_phrase == 'question':
        return answer(command)
    elif type_phrase == 'confirm':
        confirm()
    elif type_phrase == 'continue':
        do_continue()
    elif type_phrase == 'repeat':
        repeat()
    elif type_phrase == 'repeat_options':
        repeat_options()
    elif type_phrase == 'deny':
        deny()
    else:
        raise ValueError('Missing value')
