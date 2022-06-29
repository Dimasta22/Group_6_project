from solver_note_book import Notebook, Record, Title, Note, Tag
from parser import parser_notebook, similar
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
        if not text:
            return 'Введите запись'
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
            return 'Запись прошла успешно'
        elif what == 'read':
            try:
                with open(file_name, "rb") as fh:
                    file_notes = pickle.load(fh)
                    notes.extend(file_notes)
                return 'База данных успешно загружена'
            except:
                return 'Файл не создан'
        else:
            return 'Выберите или read или write'

    elif parser_notebook(sentence) == 'find':
        _, *text = sentence.split(' ')
        text = ' '.join([word for word in text])
        output_list = []
        output_str = ''
        for note in notes:
            for value in note.values():
                if re.findall(fr'{text}', f'{value}'):
                    output_list.append(note)
                    break

        for note in output_list:
            if note.get('tags', None):
                output_str += '{0}: {1}; {2}.\n'.format(note['title'], note['note'], ', '.join(note['tags']))
            else:
                output_str += '{0}: {1}.\n'.format(note['title'], note['note'])
        return output_str[:-1]

    elif parser_notebook(sentence) == 'remove':
        _, title, *args = sentence.split(' ')
        for note in notes:
            if note['title'] == title:
                notes.remove(note)
                return 'Удалено успешно'
        return 'Такой заметки нет'

    elif parser_notebook(sentence) == 'change':
        _, command, title, *args = sentence.split(' ')
        for note in notes:
            args = ' '.join([word for word in args])
            if command == 'title':
                if note['title'] == title:
                    note['note'] = args
                    return 'Заголовок замене'
            elif command == 'tag':
                old_tag, new_tag, *args = args.split(' ')
                if note.get('tags', None):
                    for tag in note.get('tags', None):
                        if tag == old_tag:
                            note['tags'].remove(old_tag)
                            note['tags'].append(new_tag)
                            return 'Тег заменен'
            else:
                return 'Комманда не верная'

    elif parser_notebook(sentence) == 'add':
        _, title, tag, *args = sentence.split(' ')
        for note in notes:
            if note['title'] == title:
                if note.get('tags', None):
                    note['tags'].append(tag)
                else:
                    note.update({'tags': [tag]})
        return 'Тэг добавлен'

    elif parser_notebook(sentence) == 'sort':
        _, title, *args = sentence.split(' ')
        for note in notes:
            if note['title'] == title:
                note['tags'] = sorted(note['tags'])

    elif parser_notebook(sentence) == 'show':
        _, *args = sentence.split(' ')
        output = ''
        for note in notes:
            record = Record(Title(note['title']), Note(note['note']))
            if note.get('tags', None):
                for tag in note['tags']:
                    record.add_tag(Tag(tag))
            output += '{0} \n'.format(str(record))
        return output[:-1]

    else:
        return similar(sentence, 'note')


if __name__ == '__main__':
    sen = 'create Gang This is game.'
    print(handler(sen))
    sen = 'create Band kiki bola sur emi'
    print(handler(sen))
    sen = 'add Band nnn'
    print(handler(sen))
    sen = 'add Gang mmm'
    print(handler(sen))
    print(notes)
    sen = 'create Band'
    print(handler(sen))
    print(notes)




