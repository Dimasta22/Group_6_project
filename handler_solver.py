from error_processing import input_error
from parser import parser_notebook
from solver_notebook import Notebook, Note, Tag, Record


NOTES = Notebook()


#@input_error
def handler(sentence):
    if parser_notebook(sentence) == 'create':
        _, tag, *note = sentence.split(' ')
        note = ' '.join([word for word in note])
        record = Record(Tag(tag), Note(note))
        NOTES[tag] = record
        return f'{tag}: {note}'

    elif parser_notebook(sentence) == 'add':
        _, tag, *note = sentence.split(' ')
        note = ' '.join([word for word in note])
        NOTES[tag].add_note(note)
        return f'{tag}: {note}'

    elif parser_notebook(sentence) == 'change':
        _, tag, *note = sentence.split(' ')
        note = ' '.join([word for word in note])
        NOTES[tag].add_note(note)
        return f'{tag}: {note}'


if __name__ == '__main__':
    sen = 'create #hi'
    print(handler(sen))