from error_processing import input_error
from solver_address_book import AddressBook, Name, Phone, Record, Birthday
from parser import parser


CONTACTS = AddressBook()


@input_error
def handler(sentence):
    if parser(sentence) == 'hello':
        return "Как я могу Вам помочь?"

    elif parser(sentence) == 'create':
        _, name, *args = sentence.split(' ')
        if len(args) == 1:
            number = args[0]
            record = Record(Name(name), Phone(number))
        elif len(args) >= 2:
            number, date = args[0], args[1]
            record = Record(Name(name), Phone(number), Birthday(date))
        else:
            record = Record(Name(name))
        for contact in CONTACTS:
            if contact == name:
                return 'Такой пользователь уже есть'
            # CONTACTS[name.value].add_phone(phone)
        CONTACTS.add_record(record)
        return 'Пользователь добавлен'

    elif parser(sentence) == 'add':
        _, name, phone, *args = sentence.split(' ')
        phone = Phone(phone)
        for k, v in CONTACTS.items():
            if k == name:
                if CONTACTS[k].add_phone(phone):
                    return "Номер добавлен"
                else:
                    return "Такой номер уже есть"
        return "Такого пользователя нет, чтобы добавить ему номер"

    elif parser(sentence) == 'change':
        _, name, old_phone, new_phone, *args = sentence.split(' ')
        name = Name(name)
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)
        for key in CONTACTS:
            if key == name.value:
                if CONTACTS[key].change_phone(old_phone, new_phone):
                    return "Номер изменен"
                else:
                    return "Такого номера нет"
                #CONTACTS[key].change_phone(old_phone, new_phone)
        return "Такого пользователя не найдено"

    elif parser(sentence) == 'delete':
        _, name, phone_to_delete, *args = sentence.split(' ')
        name = Name(name)
        phone_to_delete = Phone(phone_to_delete)
        for key in CONTACTS:
            if key == name.value:
                if CONTACTS[key].delete(phone_to_delete):
                    return "Номер удален"
                else:
                    return "Такого номера нет"
        return "Такого пользователя или номера не найдено"

    elif parser(sentence) == 'phone':
        _, name, *args = sentence.split(' ')
        if CONTACTS == {}:
            return "Список пустой"
        else:
            for key in CONTACTS:
                if key == name:
                    return f"Номерa {key} : {CONTACTS[key].phones_in_str()}"
            return "Такого контакта не найдено"

    elif parser(sentence) == 'birthday':
        _, name, *args = sentence.split(' ')
        if CONTACTS == {}:
            return "Список пустой"
        else:
            for key in CONTACTS:
                if key == name:
                    try:
                        return f"Дней до дня рождения {key} : {CONTACTS[key].days_to_birthday()}"
                    except:
                        return "У этого пользователя не указан день рождения"
            return "Такого контакта не найдено"

    elif parser(sentence) == 'show':
        _, number, *args = sentence.split(' ')
        str_ = ''
        amount = int(number)
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

    elif parser(sentence) == 'show all':
        str_ = ''
        if CONTACTS == {}:
            return "Список пустой"
        else:
            for key, value in CONTACTS.items():
                try:
                    str2 = ''
                    for phone in value.phones:
                        str2 += phone.value + ' '
                    str_ += str(value.name.value) + " : " + str(str2) + ' '
                    # Тут попробуй сделать через (f'{}', ).format, везде где str_ и str2
                except AttributeError:
                    str_ += str(value.name.value) + " : " + \
                        str(value.phones) + ' '
                try:
                    str_ += 'birthday: ' + \
                        value.birthday.value.strftime('%d.%m.%Y') + '\n'
                except:
                    str_ += '\n'
                    continue
            return str_[:-1]

    elif parser(sentence) == 'file':
        _, flag, *args = sentence.split(' ')
        # Тут будет запись и считывание файла

    elif parser(sentence) == 'find':
        _, find_it, *args = sentence.split(' ')
        if find_it == ' ':
            return 'Введите данные для поиска'
        str_ = ''
        flag = 0
        if CONTACTS == {}:
            return "Список пустой"
        else:
            for key, value in CONTACTS.items():
                flag = 0
                for phone in value.phones:
                    if find_it in phone.value:
                        flag = 1
                try:
                    if find_it in value.birthday.value.strftime('%d.%m.%Y'):
                        flag = 1
                except:
                    pass
                if find_it in key or flag == 1:
                    try:
                        str2 = ''
                        for phone in value.phones:
                            str2 += phone.value + ' '
                        str_ += str(value.name.value) + " : " + str(str2) + ' '
                    except AttributeError:
                        str_ += str(value.name.value) + " : " + \
                            str(value.phones) + ' '
                    try:
                        str_ += 'birthday: ' + \
                            value.birthday.value.strftime('%d.%m.%Y') + '\n'
                    except:
                        str_ += '\n'
                        continue

        return str_[:-1]

    elif parser(sentence) is None:
        return 'Введите команду из списка доступных команд!'


if __name__ == '__main__':
    sen = 'find delete Dima 167 050 789 87joi odi'
    print(handler(sen))
