from error_processing import input_error
from solver import AddressBook, Name, Phone, Record, Birthday
from parser import parser


@input_error
def greetings(*args, **kwargs):
    return "Как я могу Вам помочь?"


# CONTACTS = {}
CONTACTS = AddressBook()


@input_error
def new_contact(*args, **kwargs):
    information = args[0]
    name = Name(information[0])
    try:
        phone = Phone(information[1])
    except:
        phone = Phone('-')
    try:
        birthday = Birthday(information[-1])
        rec = Record(name, phone, birthday)
        flag = 1
    except:
        rec = Record(name, phone)
        flag = 0
    # rec2 = Record(name, phone2)
    CONTACTS.add_record(rec)
    for i, p in enumerate(information):
        if i == 0:
            continue
        if flag == 1 and i == len(information) - 1:
            continue
        phone = Phone(p)
        CONTACTS[name.value].add_phone(phone)
    return f"Пользователь {name.value} добавлен"


@input_error
def change_phone(*args, **kwargs):
    information = args[0]
    name = Name(information[0])
    phone = Phone(information[1])
    phone2 = Phone(information[2])
    # rec = Record(name, phone)
    for k, v in CONTACTS.items():
        if k == name.value:
            CONTACTS[k].change2_phone(phone, phone2)
            return "Номер изменен"
    return "Такого пользователя не найдено"


@input_error
def show_all(*args, **kwargs):
    str_ = ''
    if CONTACTS == {}:
        return "Список пустой"
    else:
        for k, v in CONTACTS.items():
            try:
                str2 = ''
                for p in v.phones:
                    str2 += p.value + ' '
                str_ += str(v.name.value) + " : " + \
                        str(str2) + ' '
            except AttributeError:
                str_ += str(v.name.value) + " : " + str(v.phones) + ' '
            try:
                str_ += 'birthday: ' + \
                        v.birthday.value.strftime('%d/%m/%Y') + '\n'
            except:
                str_ += '\n'
                continue
        return str_[:-1]


@input_error
def delete_contact(*args, **kwargs):
    information = args[0]
    name = Name(information[0])
    phone = Phone(information[1])
    for k, v in CONTACTS.items():
        if k == name.value:
            CONTACTS[k].delete(phone)
            return "Номер удален"
    return "Такого пользователя или номера не найдено"


@input_error
def show_phone(*args, **kwargs):
    information = args[0]
    str_ = ''
    if CONTACTS == {}:
        return "Список пустой"
    else:
        for k, v in CONTACTS.items():
            if k == information[0]:
                return f"Номерa {k} : {CONTACTS[k].phones_in_str()}"
        return "Такого контакта не найдено"


def days_to_birthday(*args, **kwargs):
    information = args[0]
    str_ = ''
    if CONTACTS == {}:
        return "Список пустой"
    else:
        for k, v in CONTACTS.items():
            if k == information[0]:
                try:
                    return f"Дней до дня рождения {k} : {CONTACTS[k].days_to_birthday()}"
                except:
                    return "У этого пользователя не указан день рождения"
        return "Такого контакта не найдено"


@input_error
def show(*args, **kwargs):
    str_ = ''
    inf = args[0]
    amount = int(inf[0])
    border = 0
    if CONTACTS == {}:
        return "Список пустой"
    else:
        while True:
            if amount != border:
                str_ += str(next(CONTACTS)) + '\n'
                border += 1
            else:
                break
    return str_[:-1]


def open_and_save_file(flag=0):
    filename = 'contacts'
    save_str = ''
    if flag == 1:
        # запись
        CONTACTS.write()
    else:
        # чтение
        CONTACTS.read()


def find(*args, **kwargs):
    information = args[0]

    if information is []:
        return show_all()

    str_ = ''
    flag = 0
    phones = []
    if CONTACTS == {}:
        return "Список пустой"
    else:
        for k, v in CONTACTS.items():
            for p in v.phones:
                if information[0] in p.value:
                    flag = 1
            try:
                if information[0] in v.birthday.value.strftime('%d/%m/%Y'):
                    flag = 1
            except:
                pass
            if information[0] in k or flag == 1:
                try:
                    str2 = ''
                    for p in v.phones:
                        str2 += p.value + ' '
                    str_ += str(v.name.value) + " : " + \
                            str(str2) + ' '
                except AttributeError:
                    str_ += str(v.name.value) + " : " + str(v.phones) + ' '
                try:
                    str_ += 'birthday: ' + \
                            v.birthday.value.strftime('%d/%m/%Y') + '\n'
                except:
                    str_ += '\n'
                    continue
            phones = []
            flag = 0
    return str_[:-1]



