import re


COMMANDS_ADDRESSBOOK = [
    'hello',
    'create',
    'add',
    'show all',
    'change',
    'phone',
    'delete',
    'birthday',
    'show',
    'find',
    'exit',
    'close',
    'good bye'
]

COMMANDS_NOTEBOOK = [
    # Тут будут команды для работы с записником
]

COMMANDS_JOB = [
    'addressbook',
    'notebook'
]


def parser(sentence):
    sentence = sentence.lower().strip()
    for key in COMMANDS_ADDRESSBOOK:
        func = re.search(fr'^{key}\b', sentence)
        if func is not None:
            return func.group()


def parser_job(sentence):
    sentence = sentence.lower().strip()
    for key in COMMANDS_JOB:
        func = re.search(fr'^{key}\b', sentence)
        if func is not None:
            return func.group()


def arg(sentence):
     _, name, old_phone, new_phone, *args = sentence.split(' ')
     return args


if __name__ == '__main__':
    sen = 'show Dima 167 050 789 87joi odi'
    print(parser(sen))
    print(arg(sen))