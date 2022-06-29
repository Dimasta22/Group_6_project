from error_processing import input_error
from solver_address_book import AddressBook, Name, Phone, Record, Birthday, Email, Address
from parser import parser, similar
import re
import os

CONTACTS = AddressBook()


def create_contact(sentence):
    name, *args = sentence.split(' ')
    name = Name(name)
    phone = None
    phones = []
    birthday = None
    email = None
    emails = []
    addresses = []
    address = None
    re_birthday = '\d{2}\.\d{2}\.\d{4}'
    re_address = '[a-zA-Zа-яА-ЯёЁЇїІіЄєҐґ_]{2,}\.[a-zA-Zа-яА-Я ёЁЇїІіЄєҐґ_]{2,}\/[0-9a-zA-Zа-яА-Я \/ёЁЇїІіЄєҐґ_]{0,100}'
    for arg in args:
        if re.match(r"\d{12}|\d{10}|\d{3}", arg) is not None:
            phone = Phone(arg)
            phones.append(phone)
        elif re.match(r"[a-zA-Z][a-zA-Z0-9_.]{1,}@\w+[.][a-z]{2,}", arg) is not None:
            email = Email(arg)
            emails.append(email)
        elif re.match(re_birthday, arg) is not None:
            birthday = Birthday(arg)
        elif re.match(re_address, arg) is not None:
            address = Address(arg.replace('_', ' '))
            addresses.append(address)
        else:
            return f'{arg} не подходит по формату'
    record = Record(name, phone, birthday, email)
    CONTACTS.add_record(record)
    for phone in phones:
        CONTACTS[name.value].add_phone(phone)
    for email in emails:
        CONTACTS[name.value].add_email(email)
    for address in addresses:
        CONTACTS[name.value].add_address(address)
    return 'Пользователь добавлен'


@input_error
def handler(sentence):
    if parser(sentence) == 'hello':
        return "Как я могу Вам помочь?"

    elif parser(sentence) == 'create':
        sentence = sentence.split(' ')
        sentence.pop(0)
        sentence = ' '.join(sentence)
        return create_contact(sentence)

    elif parser(sentence) == 'add':
        _, name, phone, *args = sentence.split(' ')
        phone = Phone(phone)
        for k, v in CONTACTS.items():
            if k == name:
                if CONTACTS[k].add_phone(phone):
                    return "Номер добавлен"
                else:
                    return "Такой номер уже есть"
        return "Такого пользователя нет, чтобы добавить ему"

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
                # CONTACTS[key].change_phone(old_phone, new_phone)
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
                    str_ += str(value.name.value)+' '
                    for phone in value.phones:
                        str2 += phone.value + ' '
                    if str2 != '':
                        str_ += " : " + str(str2) + ' '
                    else:
                        str_ += ''
                except AttributeError:
                    str_ += str(value.name.value) + " : " + \
                        str(value.phones) + ' '
                try:
                    str_ += 'birthday: ' + \
                        value.birthday.value.strftime('%d.%m.%Y') + ' '
                except:
                    str_ += ' '
                try:
                    str2 = ''
                    for email in value.emails:
                        str2 += email.value + ' '
                    if str2 != '':
                        str_ += 'email: ' + str(str2) + ' '
                    else:
                        str_ += ' '
                except:
                    str_ += ' '
                try:
                    str2 = ''
                    for address in value.addresses:
                        str2 += address.value + ' '
                    if str2 != '':
                        str_ += 'addresses: ' + str(str2) + '\n'
                    else:
                        str_ += '\n'
                except:
                    str_ += '\n'
                    continue
            return str_[:-1]

    elif parser(sentence) == 'file':
        _, flag, *args = sentence.split(' ')
        if flag == 'write':
            try:
                os.remove('contacts.dir')
                os.remove('contacts.dat')
                os.remove('contacts.bak')
            except:
                pass
            CONTACTS.write()
            return 'Книга контактов сохранена'
        elif flag == 'read':
            contacts_in_str = CONTACTS.read()
            if contacts_in_str[0] == '':
                return 'Файл пустой'
            for contact in contacts_in_str:
                create_contact(contact)
            return 'Книга контактов загружена'
    elif parser(sentence) == 'remove':
        _, key, *args = sentence.split(' ')
        try:
            CONTACTS.pop(key)
        except:
            return 'Такого контакта нет в адресной книге'
        return f'Контакт {key} удален из адресной книги'
    elif parser(sentence) == 'find':
        _, find_it, *args = sentence.split(' ')
        if find_it == ' ':
            return 'Введите данные для поиска'
        str_ = ''
        if CONTACTS == {}:
            return "Список пустой"
        else:
            for key, value in CONTACTS.items():
                flag = 0
                for phone in value.phones:
                    if find_it in phone.value:
                        flag = 1
                for email in value.emails:
                    if find_it in email.value:
                        flag = 1
                for addres in value.addresses:
                    if find_it in addres.value:
                        flag = 1
                try:
                    if find_it in value.birthday.value.strftime('%d.%m.%Y'):
                        flag = 1
                except:
                    pass
                if find_it in key or flag == 1:
                    try:
                        str2 = ''
                        str_ += str(value.name.value)+' '
                        for phone in value.phones:
                            str2 += phone.value + ' '
                        if str2 != '':
                            str_ += " : " + str(str2) + ' '
                        else:
                            str_ += ''
                    except AttributeError:
                        str_ += str(value.name.value) + " : " + \
                            str(value.phones) + ' '
                    try:
                        str_ += 'birthday: ' + \
                            value.birthday.value.strftime('%d.%m.%Y') + ' '
                    except:
                        str_ += ' '
                    try:
                        str2 = ''
                        for email in value.emails:
                            str2 += email.value + ' '
                        if str2 != '':
                            str_ += 'email: ' + str(str2) + ' '
                        else:
                            str_ += ' '
                    except:
                        str_ += ' '
                    try:
                        str2 = ''
                        for address in value.addresses:
                            str2 += address.value + ' '
                        if str2 != '':
                            str_ += 'addresses: ' + str(str2) + '\n'
                        else:
                            str_ += '\n'
                    except:
                        str_ += '\n'
                        continue

        return str_[:-1]
    else:
        return similar(sentence, 'address')


if __name__ == '__main__':
    sen = 'find delete Dima 167 050 789 87joi odi'
    print(handler(sen))
