from datetime import datetime
from error_processing import input_error
from collections import UserDict
from itertools import islice


class Field:
    def __init__(self, value) -> None:
        self.value = value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


@ input_error
class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        value = value.strip()
        for ch in value:
            if ch not in "0123456789()-+":
                raise ValueError("Invalid phone number")
        self.__value = value


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, b_value):
        if b_value:
            try:
                b_value = datetime.strptime(b_value, '%d.%m.%Y')
            except ValueError:
                raise ValueError("Invalid birthday")
        self.__value = b_value


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
            year=today.year+1, month=self.birthday.value.month, day=self.birthday.value.day)
        bd_in_this_year = datetime(
            year=today.year, month=self.birthday.value.month, day=self.birthday.value.day)
        if bd_in_this_year > today:
            difference = bd_in_this_year-today
        else:
            difference = bd_in_year-today
        return difference.days

    def change_phone(self, phone: Phone, new_phone: Phone) -> bool:
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
            str_ += str(p.value)+' '
        return str_[:-1]


class AddressBook(UserDict):
    current_amount = 0
    filename = 'contacts'
    save_str = ''

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
                str_ += ', день рождения: '+self.data[keys_data[self.current_amount]
                                                      ].birthday.value.strftime('%d/%m/%Y')+'\n'
            except:
                str_ += '\n'
            self.current_amount += 1
            return str_[:-1]
        raise StopIteration


if __name__ == '__main__':
    person_name = Name('Jeka')
    person_phone = Phone('259+++8')
    person_1 = Record(person_name, person_phone)
    print(person_1)
    print(AddressBook().add_record(person_1))
