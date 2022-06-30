from collections import UserDict


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
        self.note = note
        self.tags = []
        if tag:
            self.tags.append(tag)

    def __str__(self):
        return '{0}: {1}; {2}.'.format(self.title,
                                       self.note,
                                       ", ".join([tag.value for tag in self.tags]))

    def add_tag(self, tag: Tag) -> None:
        self.tags.append(tag)

    def delete_tag(self, tag: Tag) -> None:
        self.tags.remove(tag)


class Notebook(UserDict):
    def add_record(self, record: Record) -> None:
        if record.tags:
            self.data.update({'title': record.title.value, 'note': record.note.value,
                              'tags': [", ".join([tag.value for tag in record.tags])]})
        else:
            self.data.update({'title': record.title.value, 'note': record.note.value})

        '''
        self.data['title'] = record.title.value
        self.data['note'] = record.note.value
        self.data['tags'] = [", ".join([tag.value for tag in record.tags])]
        '''


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
    #print(all_notes['tags'])
    #all_notes['tags'].add_tag(Tag('yu'))
    print(all_notes['title'])
    print(all_notes['note'])
    print(all_notes['tags'])
    record1.add_tag(Tag('aaa'))
    print(record1)
    #print(Record(all_notes['title'], all_notes['note'], all_notes['tags']))
