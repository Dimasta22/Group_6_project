from ast import arg
from collections import UserDict
from datetime import datetime
from datetime import date
from itertools import islice
from os import stat
import shelve


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except IndexError:
            return "Вы ввели не полные данные"
        except TypeError:
            return "Вы ввели что-то лишнее"
        except KeyError:
            return "Вы ввели не полные данные. Попробуйте снова"
        except StopIteration:
            return "Столько контактов нет"
        return result

    return inner


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value


class Name(Field):
    # name = ''
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value and type(value) is str:
            self.__value = value
        else:
            raise ValueError('Invalid name')


class Birthday(Field):
    # name = ''
    # def __init__(self, birthday) -> None:
    #     self.birthday = datetime.strptime(birthday, '%d/%m/%Y')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, b_value):
        if b_value:
            try:
                b_value = datetime.strptime(b_value, '%d/%m/%Y')
            except ValueError:
                raise ValueError("Invalid birthday")
        self.__value = b_value


@input_error
class Phone(Field):
    # def __init__(self, phone=None) -> None:
    #     self.phone = phone
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, n_value):
        n_value = n_value.strip()
        for ch in n_value:
            if ch not in "0123456789()-+":
                raise ValueError("Invalid phone number")
        self.__value = n_value


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.add_phone(phone)

    def days_to_birthday(self):
        today = datetime.now()
        bd_in_year = datetime(
            year=today.year + 1, month=self.birthday.value.month, day=self.birthday.value.day)
        bd_in_this_year = datetime(
            year=today.year, month=self.birthday.value.month, day=self.birthday.value.day)
        if bd_in_this_year > today:
            difference = bd_in_this_year - today
        else:
            difference = bd_in_year - today
        return difference.days

    def change2_phone(self, phone: Phone, new_phone: Phone) -> bool:
        for p in self.phones:
            if phone.value == p.value:
                self.delete(phone)
                self.add_phone(new_phone)
                return True
            return False

    def delete(self, phone) -> bool:
        for i, p in enumerate(self.phones):
            if str(p.value) == str(phone.value):
                self.phones.pop(i)
                # self.phones[i] = '-'
                return True
        return False

    def add_phone(self, phone) -> bool:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return True
        return False

    def phones_in_str(self):
        str_ = ''
        for p in self.phones:
            str_ += str(p.value) + ' '
        return str_[:-1]


class AddressBook(UserDict):
    current_amount = 0
    filename = 'contacts'
    save_str = ''

    def write(self):
        # запись
        with shelve.open(self.filename) as states:
            for k, v in self.data.items():
                print(k)
                self.save_str += k + ','
                for p in v.phones:
                    self.save_str += p.value + ','
                try:
                    self.save_str += v.birthday.value.strftime('%d/%m/%Y') + ','
                except:
                    self.save_str += ''
                states[k] = self.save_str[:-1]
                self.save_str = ''

    def read(self):
        # чтение
        with shelve.open(self.filename) as states:
            for key in states:
                value = states[key].split(',')
                # value = (value,)
                new_contact(value)

    def add_record(self, rec):
        self.data[rec.name.value] = rec

    def __iter__(self):
        return super().__iter__()

    def __next__(self):
        str_ = ''
        keys_data = list(islice(self.data, None))
        if self.current_amount != len(self.data):
            str_ += "Контакт " + \
                    self.data[keys_data[self.current_amount]].name.value + ' : '
            str_ += self.data[keys_data[self.current_amount]
            ].phones_in_str()
            try:
                str_ += ', день рождения: ' + self.data[keys_data[self.current_amount]
                                                        ].birthday.value.strftime('%d/%m/%Y') + '\n'

            except:
                str_ += '\n'
            self.current_amount += 1
            return str_[:-1]
        raise StopIteration


@input_error
def parser(str_: str):
    listik = str_.split(' ')
    if str_.lower() == 'show all':
        return str_.lower(), []
    elif listik[0].lower() in COMMANDS:
        command = listik[0].lower()
        del listik[0]
        return command, listik


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


def main():
    open_and_save_file(0)
    exit_words = ["good bye", "close", "exit", '.']
    kort = None  # будующий кортеж где первый эллемент - команда, воторой - данные
    while True:
        command = input("Введите команду: ")
        if command.lower() in exit_words:
            print("Bye")
            break
        kort = parser(command)
        if kort is None:
            print(f"Команды {command} не найдено")
            continue
        handler = get_handler(kort[0])
        print(handler(kort[1]))
    open_and_save_file(1)
    # print(CONTACTS)


if __name__ == "__main__":
    main()
