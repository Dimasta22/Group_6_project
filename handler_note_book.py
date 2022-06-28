from solver_note_book import Notebook, Record, Title, Note, Tag
from parser import parser_notebook
import pickle
from error_processing import input_error
import re

all_notes = Notebook()
notes = []


@input_error
def handler(sentence):
    if parser_notebook(sentence) == 'create':
        _, name, *text = sentence.split(' ')
        title = Title(name)
        note = Note(" ".join([word for word in text]))
        record = Record(title, note)
        all_notes.add_record(record)
        notes.append(all_notes.copy())
        return 'Запись добавлена'

    elif parser_notebook(sentence) == 'file':
        _, what, *text = sentence.split(' ')
        file_name = 'notebook_data.bin'

        if what == 'write':
            with open(file_name, "wb") as fh:
                pickle.dump(notes, fh)
        elif what == 'read':
            with open(file_name, "rb") as fh:
                file_notes = pickle.load(fh)
                notes.extend(file_notes)
                print(notes)
        else:
            return 'Выберите или read или write'

    elif parser_notebook(sentence) == 'find':
        _, *text = sentence.split(' ')
        text = ' '.join([word for word in text])
        for note in notes:
            for value in note.values():
                if re.findall(fr'{text}', f'{value}'):

                    #print(f'{note}')
                    break
        return 'Нашлись эти записи'

    elif parser_notebook(sentence) == 'remove':
        _, title, *args = sentence.split(' ')
        for note in notes:
            if note['title'] == title:
                notes.remove(note)
        return notes

    elif parser_notebook(sentence) == 'change':
        _, command, title, *args = sentence.split(' ')
        args = ' '.join([word for word in args])

        for note in notes:
            if command == 'title':
                if note['title'] == title:
                    note['note'] = args

            elif command == 'tag':
                old_tag, new_tag, *args = args.split(' ')
                if note.get('tags', None):
                    for tag in note.get('tags', None):
                        if tag == old_tag:
                            note['tags'].remove(old_tag)
                            note['tags'].append(new_tag)

    elif parser_notebook(sentence) == 'add':
        _, title, tag, *args = sentence.split(' ')
        for note in notes:
            if note.get('tags', None):
                note['tags'].append(tag)
            else:
                record = Record(Title(note['title']), Note(note['note']), Tag(tag))
                notes.remove(note)
                all_notes.add_record(record)
                notes.append(all_notes.copy())

    elif parser_notebook(sentence) == 'sort':
        _, title, *args = sentence.split(' ')
        for note in notes:
            if note['title'] == title:
                note['tags'] = sorted(note['tags'])


if __name__ == '__main__':
    sen = 'create Gang This is game.'
    print(handler(sen))
    sen = 'create Band kiki bola sur emi'
    print(handler(sen))
    print(notes)
    sen = 'file'
    print(handler(sen))
    sen = 'find ang'
    print(handler(sen))
    sen = 'remove Gang'
    print(handler(sen))
    sen = 'change title Band zuzu lilu baka'
    print(handler(sen))
    print(notes)
    sen = 'add Band Africa'
    print(handler(sen))
    print(notes)
    sen = 'change tag Band Africa Ukraine'
    print(handler(sen))
    print(notes)
    sen = 'add Band Africa'
    print(handler(sen))
    print(notes)
    sen = 'sort Band Africa'
    print(handler(sen))
    print(notes)



