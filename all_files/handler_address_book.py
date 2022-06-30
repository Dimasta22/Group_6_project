from distutils.sysconfig import get_python_lib
from .error_processing import input_error
from .solver_address_book import AddressBook, Name, Phone, Record, Birthday, Email, Address
from .parser import parser, similar
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
            return f'{arg} does not fit the format'
    record = Record(name, phone, birthday, email)
    CONTACTS.add_record(record)
    for phone in phones:
        CONTACTS[name.value].add_phone(phone)
    for email in emails:
        CONTACTS[name.value].add_email(email)
    for address in addresses:
        CONTACTS[name.value].add_address(address)
    return 'User added'


@input_error
def handler(sentence):
    if parser(sentence) == 'hello':
        return "How can I help you?"

    elif parser(sentence) == 'create':
        sentence = sentence.split(' ')
        sentence.pop(0)
        sentence = ' '.join(sentence)
        return create_contact(sentence)

    elif parser(sentence) == 'add phone':
        _, _, name, phone, *args = sentence.split(' ')
        phone = Phone(phone)
        for k, v in CONTACTS.items():
            if k == name:
                if CONTACTS[k].add_phone(phone):
                    return "Number added"
                else:
                    return "This number already exists."
        return "There is no such user"

    elif parser(sentence) == 'add email':
        _, _, name, email, *args = sentence.split(' ')
        email = Email(email)
        for key, value in CONTACTS.items():
            if key == name:
                if CONTACTS[key].add_email(email):
                    return "Added email"
                else:
                    return "This email is already created"
        return "There is no such user"

    elif parser(sentence) == 'add address':
        _, _, name, address, *args = sentence.split(' ')
        address = Address(address)
        for key, value in CONTACTS.items():
            if key == name:
                if CONTACTS[key].add_address(address):
                    return "Added address"
                else:
                    return "This address is already created"
        return "There is no such user"

    elif parser(sentence) == 'add birthday':
        _, _, name, birthday, *args = sentence.split(' ')
        birthday = Birthday(birthday)
        for key, value in CONTACTS.items():
            if key == name:
                if CONTACTS[name].add_birthday(birthday):
                    return "Added birthday"
                else:
                    return "This birthday is already created"
        return "There is no such user"

    elif parser(sentence) == 'change phone':
        _, _, name, old_phone, new_phone, *args = sentence.split(' ')
        name = Name(name)
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)
        for key in CONTACTS:
            if key == name.value:
                if CONTACTS[key].change_phone(old_phone, new_phone):
                    return "Number changed"
                else:
                    return "No such number"
        return "No such user found"

    elif parser(sentence) == 'change email':
        _, _, name, old_email, new_email, *args = sentence.split(' ')
        # name = Name(name)
        old_email = Email(old_email)
        new_email = Email(new_email)
        for key in CONTACTS:
            if key == name:
                if CONTACTS[key].change_email(old_email, new_email):
                    return "Email is changed"
                else:
                    return "No such email"
        return "No such user found"

    elif parser(sentence) == 'change address':
        _, _, name, old_address, new_address, *args = sentence.split(' ')
        name = Name(name)
        old_address = Address(old_address)
        new_address = Address(new_address)
        for key in CONTACTS:
            if key == name.value:
                if CONTACTS[key].change_address(old_address, new_address):
                    return "Address is changed"
                else:
                    return "No such address"
        return "No such user found"

    elif parser(sentence) == 'delete phone':
        _, _, name, phone_to_delete, *args = sentence.split(' ')
        name = Name(name)
        phone_to_delete = Phone(phone_to_delete)
        for key in CONTACTS:
            if key == name.value:
                if CONTACTS[key].delete_phone(phone_to_delete):
                    return "Number removed"
                else:
                    return "No such number"
        return "No such user found"

    elif parser(sentence) == 'delete email':
        _, _, name, email_to_delete, *args = sentence.split(' ')
        name = Name(name)
        email_to_delete = Email(email_to_delete)
        for key in CONTACTS:
            if key == name.value:
                if CONTACTS[key].delete_email(email_to_delete):
                    return "Email deleted"
                else:
                    return "No such email"
        return "No such user found"

    elif parser(sentence) == 'delete address':
        _, _, name, address_to_delete, *args = sentence.split(' ')
        name = Name(name)
        address_to_delete = Address(address_to_delete)
        for key in CONTACTS:
            if key == name.value:
                if CONTACTS[key].delete_address(address_to_delete):
                    return "Address deleted"
                else:
                    return "No such address"
        return "No such user found"

    elif parser(sentence) == 'phone':
        _, name, *args = sentence.split(' ')
        if CONTACTS == {}:
            return "List is empty"
        else:
            for key in CONTACTS:
                if key == name:
                    return f"Numbers {key} : {CONTACTS[key].phones_in_str()}"
            return "No such contact found"

    elif parser(sentence) == 'birthday':
        _, name, *args = sentence.split(' ')
        if CONTACTS == {}:
            return "List is empty"
        else:
            for key in CONTACTS:
                if key == name:
                    try:
                        return f"Days to birthday {key} : {CONTACTS[key].days_to_birthday()}"
                    except:
                        return "This user does not have a birthday"
            return "No such user found"

    elif parser(sentence) == 'show':
        _, number, *args = sentence.split(' ')
        str_ = ''
        amount = int(number)
        border = 0
        if CONTACTS == {}:
            return "List is empty"
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
            return "List is empty"
        else:
            for key, value in CONTACTS.items():
                try:
                    str2 = ''
                    str_ += str(value.name.value) + ' '
                    for phone in value.phones:
                        str2 += phone.value + ', '
                    if str2 != '':
                        str_ += ": phones: " + str(str2[:-2]) + '; '
                    else:
                        str_ += ''
                except AttributeError:
                    str_ += str(value.name.value) + " : " + \
                        str(value.phones) + ' '
                try:
                    str_ += 'birthday: ' + \
                        value.birthday.value.strftime('%d.%m.%Y') + '; '
                except:
                    str_ += ' '
                try:
                    str2 = ''
                    for email in value.emails:
                        str2 += email.value + ', '
                    if str2 != '':
                        str_ += 'emails: ' + str(str2[:-2]) + '; '
                    else:
                        str_ += ' '
                except:
                    str_ += ' '
                try:
                    str2 = ''
                    for address in value.addresses:
                        str2 += address.value + ', '
                    if str2 != '':
                        str_ += 'addresses: ' + str(str2[:-2]) + '.\n'
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
            return 'Contact book saved'
        elif flag == 'read':
            contacts_in_str = CONTACTS.read()
            if contacts_in_str[0] == '':
                return 'File is empty'
            for contact in contacts_in_str:
                create_contact(contact)
            return 'Contact book loaded'
    elif parser(sentence) == 'clear':
        _, *args = sentence.split(' ')
        CONTACTS.clear()
        try:
            os.remove('contacts.dir')
            os.remove('contacts.dat')
            os.remove('contacts.bak')
        except:
            return 'Files are absent'
        return 'Contact book cleared'

    elif parser(sentence) == 'help':
        _, *args = sentence.split(' ')
        file_name = os.path.join(get_python_lib(), 'all_files', 'addressbook_helper')
        with open(file_name, 'r') as file:
            text = file.readlines()
            text = ' '.join(text)
        return text

    elif parser(sentence) == 'remove':
        _, key, *args = sentence.split(' ')
        try:
            CONTACTS.pop(key)
        except:
            return 'This contact is not in the address book'
        return f'Contact {key} removed from address book'

    elif parser(sentence) == 'find':
        _, find_it, *args = sentence.split(' ')
        if find_it == ' ':
            return 'Enter data to search'
        str_ = ''
        if CONTACTS == {}:
            return "List is empty"
        else:
            for key, value in CONTACTS.items():
                flag = 0
                for phone in value.phones:
                    if find_it in phone.value:
                        flag = 1
                for email in value.emails:
                    if find_it in email.value:
                        flag = 1
                for address in value.addresses:
                    if find_it in address.value:
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
