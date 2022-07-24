from datetime import datetime
from error_processing import input_error
from collections import UserDict
from itertools import islice
import shelve
import re


class Field:
    def __init__(self, value) -> None:
        self.value = value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)


class Email(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        is_email = re.search(
            r"[a-zA-Z][a-zA-Z0-9_.]{1,}@\w+[.][a-z]{2,}", value)
        if is_email == None or len(value) != is_email.end():
            raise ValueError("Invalid email format")
        self.__value = value


class Address(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        if re.match(r"[a-zA-Zа-яА-ЯёЁЇїІіЄєҐґ_]{2,}\.[a-zA-Zа-яА-Я ёЁЇїІіЄєҐґ_]{2,}\/[0-9a-zA-Zа-яА-Я \/ёЁЇїІіЄєҐґ_]{0,100}", value) is None:
            raise ValueError("Invalid address format")
        self.__value = value


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
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None, address: Address = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.addresses = []
        self.emails = []
        if phone:
            self.add_phone(phone)
        elif email:
            self.add_email(email)
        elif address:
            self.add_address(address)

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
                self.delete_phone(phone)
                self.add_phone(new_phone)
                return True
        return False

    def change_address(self, address: Address, new_address: Address) -> bool:
        for p in self.addresses:
            if address.value == p.value:
                self.delete_address(address)
                self.add_address(new_address)
                return True
        return False

    def change_email(self, email: Email, new_email: Email) -> bool:
        for p in self.emails:
            if email.value == p.value:
                self.delete_email(email)
                self.add_email(new_email)
                return True
        return False

    def delete_phone(self, phone) -> bool:
        for i, p in enumerate(self.phones):
            if str(p.value) == str(phone.value):
                self.phones.pop(i)
                return True
        return False

    def delete_address(self, address) -> bool:
        for i, a in enumerate(self.addresses):
            if str(a.value) == str(address.value):
                self.addresses.pop(i)
                return True
        return False

    def delete_email(self, email) -> bool:
        for i, e in enumerate(self.emails):
            if str(e.value) == str(email.value):
                self.emails.pop(i)
                return True
        return False

    def add_phone(self, phone) -> bool:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return True
        return False

    def add_email(self, email) -> bool:
        if email.value not in [p.value for p in self.emails]:
            self.emails.append(email)
            return True
        return False

    def add_address(self, address) -> bool:
        if address.value not in [p.value for p in self.addresses]:
            self.addresses.append(address)
            return True
        return False

    def add_birthday(self, birthday: Birthday) -> bool:
        if self.birthday is None:
            self.birthday = birthday
            return True
        return False

    def phones_in_str(self):
        str_ = ''
        for p in self.phones:
            str_ += str(p.value)+' '
        return str_[:-1]

    def emails_in_str(self):
        str_ = ''
        for email in self.emails:
            str_ += str(email.value)+' '
        return str_[:-1]

    def addresses_in_str(self):
        str_ = ''
        for address in self.addresses:
            str_ += str(address.value)+' '
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
            str_ += "Contact " + \
                self.data[keys_data[self.current_amount]].name.value + ' : '
            str_ += self.data[keys_data[self.current_amount]
                              ].phones_in_str()
            try:
                str_ += ', birthday: ' + self.data[keys_data[self.current_amount]
                                                   ].birthday.value.strftime('%d.%m.%Y')+', '
            except:
                str_ += ' '
            try:
                str_ += 'email: ' + self.data[keys_data[self.current_amount]
                                              ].emails_in_str() + ', '
            except:
                str_ += ' '
            try:
                str_ += 'address: ' + self.data[keys_data[self.current_amount]
                                                ].addresses_in_str() + '\n'
            except:
                str_ += '\n'
            self.current_amount += 1
            return str_[:-1]
        raise StopIteration

    def write(self):
        with shelve.open(self.filename) as states:
            for k, v in self.data.items():
                self.save_str += k + ','
                if v.phones:
                    for p in v.phones:
                        self.save_str += p.value + ','
                if v.emails:
                    for email in v.emails:
                        self.save_str += email.value + ','
                if v.addresses:
                    for address in v.addresses:
                        self.save_str += address.value + ','
                try:
                    self.save_str += v.birthday.value.strftime('%d.%m.%Y')+','
                except:
                    self.save_str += ''
                states[k] = self.save_str[:-1]
                self.save_str = ''

    def read(self):
        all_contacts_from_file = ''
        with shelve.open(self.filename, flag='r') as states:
            for key in states:
                all_contacts_from_file += states[key].replace(
                    ',', ' ')+'\n'
            return(all_contacts_from_file[:-1].split('\n'))


if __name__ == '__main__':
    person_name = Name('Jeka')
    person_phone = Phone('259+++8')
    person_1 = Record(person_name, person_phone)
    print(person_1)
    print(AddressBook().add_record(person_1))
