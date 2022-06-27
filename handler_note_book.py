from solver_note_book import Notebook, Record, Title, Note, Tag
from parser import parser_notebook
import pickle
from error_processing import input_error

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
        for note in notes:
            pass


if __name__ == '__main__':
    sen = 'create Gang This is game.'
    print(handler(sen))
    sen = 'create Band kiki bola sur emi'
    print(handler(sen))
    print(notes)
    sen = 'file'
    print(handler(sen))

