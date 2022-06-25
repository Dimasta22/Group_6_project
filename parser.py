from handler import greetings, new_contact, show_all, change_phone, show_phone, \
    delete_contact, days_to_birthday, show, find


COMMANDS = {
    'hello': greetings,
    'add': new_contact,
    'show all': show_all,
    'change': change_phone,
    'phone': show_phone,
    'delete': delete_contact,
    'birthday': days_to_birthday,
    'show': show,
    'find': find,
}


def get_handler(operator):
    return COMMANDS[operator]


def parser(str_: str):
    listik = str_.split(' ')
    if str_.lower() == 'show all':
        return str_.lower(), []
    elif listik[0].lower() in COMMANDS:
        command = listik[0].lower()
        del listik[0]
        return command, listik


if __name__ == '__main__':
    sen = 'find delete Dima 167 050 789 87joi odi'
    print(parser(sen))