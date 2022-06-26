from collections import UserDict
import re


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Title(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


class Tag(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


class Note(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


class Record:
    def __init__(self, title: Title, note: Note = None, tag: Tag = None) -> None:
        self.title = title
        self.notes = []
        if note:
            self.notes.append(note)
        self.tags = []
        if tag:
            self.tags.append(tag)

    def __str__(self):
        return '{0}: {1}; {2}.'.format(self.title,
                                       ", ".join([note.value for note in self.notes]),
                                       ", ".join([tag.value for tag in self.tags]))

    def add_tag(self, tag: Tag) -> None:
        self.tags.append(tag)

    def add_note(self, note: Note) -> None:
        self.notes.append(note)

    def delete_note(self, note: Note) -> None:
        self.notes.remove(note)

    def change_note(self, note: Note, new_note: Note) -> None:
        self.notes.remove(note)
        self.notes.append(new_note)


class Notebook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data.update({'title': record.title.value,
                          'note': [", ".join([note.value for note in record.notes])],
                          'tags': [", ".join([tag.value for tag in record.tags])]})


if __name__ == "__main__":
    all_notes = Notebook()
    print(all_notes)
    title1 = Title('Football')
    note1 = Note('football math Ukraine-Italy')
    tag1 = Tag('sport')
    record1 = Record(title1, note1, tag1)
    all_notes.add_record(record1)
    print(record1)
    print(all_notes)
    all_notes['tags'].append('ss')
    print(all_notes['tags'])
    '''
    print(tag1)
    tag2 = Tag('team')
    print(tag2)
    all_notes['tags'].add_tag(tag2)
    print(all_notes)
    '''

    '''
    all_notes = Notebook()
    tag = Tag('#sport')
    note = Note('I like football, and my friends too')
    note_2 = Note('Ukraine')
    note_3 = Note('Boss')
    first_note = Record(tag, note)
    all_notes[tag] = Record(tag, note)
    #print(all_notes)
    all_notes[tag].add_note(note_2)
    all_notes[tag].change_note(note, note_3)
    all_notes[tag].delete_note(note_2)
    all_notes[Tag('#politic')] = Record(Tag('#politic'), Note('Ukraine'))
    for key in all_notes:
        print(all_notes[key])
    find = 'Bos'
    for key, value in all_notes.items():
        if re.findall(fr'{find}', f'{key}') != [] or re.findall(fr'{find}', f'{value}') != []:
            print(f'{value}')
    new_dict = {}
    for key, value in all_notes.items():
        new_dict.update({key.value: value})

    print(new_dict.items())

    print(sorted(new_dict.items()))
    sorted(new_dict.items())

    for key, value in sorted(new_dict.items()):
    print(f'{value}')
    '''