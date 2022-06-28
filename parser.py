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
    'file',
    'find',
    'exit',
    'close',
    'good bye'
]

COMMANDS_NOTEBOOK = [
    'create',
    'add',
    'change',
    'delete',
    'sort',
    'find',
    'file',
    'remove',
    'show',
    'exit',
    'close',
    'good bye'
]


def parser(sentence):
    sentence = sentence.lower().strip()
    for key in COMMANDS_ADDRESSBOOK:
        func = re.search(fr'^{key}\b', sentence)
        if func is not None:
            return func.group()


def parser_notebook(sentence):
    sentence = sentence.lower().strip()
    for key in COMMANDS_NOTEBOOK:
        func = re.search(fr'^{key}\b', sentence)
        if func is not None:
            return func.group()


if __name__ == '__main__':
    sen = 'show Dima 167 050 789 87joi odi'
    print(parser(sen))
