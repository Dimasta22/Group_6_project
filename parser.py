import re
import difflib

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
    'file',
    'close',
    'remove',
    'good bye'
]

COMMANDS_NOTEBOOK = [
    'create',
    'add',
    'change',
    'delete',
    'sort',
    'find',
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


def similar(command, which_list):
    final_command = None
    word_percents = 0
    if which_list == 'address':
        arr = COMMANDS_ADDRESSBOOK
    elif which_list == 'note':
        arr = COMMANDS_NOTEBOOK

    for i in arr:
        s = difflib.SequenceMatcher(None, i, command)
        a = s.ratio()
        if a > word_percents:
            word_percents = a
            final_command = i
    if final_command == None:
        return 'Ничего похожего не найдено'
    return f'Может вы имели ввиду команду: {final_command}'


if __name__ == '__main__':
    sen = 'show Dima 167 050 789 87joi odi'
    print(parser(sen))
