from view import *
import pickle
from collections import UserDict
from datetime import datetime
import re

ADDRESSBOOK_DB = "data.bin"
PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$)")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
NAME_REGEX = re.compile(r'^[a-zA-Zа-яА-Я]{2,20}$')
ADDRESS_REGEX = re.compile(r'^[a-zA-Zа-яА-Я0-9,. ]{2,20}$')


class Field:
    def __init__(self, value) -> None:
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return self._value


class Name(Field):
    @Field.value.setter
    def value(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not re.match(NAME_REGEX, name):
            raise ValueError('Name must be between 2 and 20 characters')
        self._value = name


class Phone(Field):
    @Field.value.setter
    def value(self, phone: str):
        if not isinstance(phone, str):
            raise TypeError('Phone must be a string')
        if bool(re.match(PHONE_REGEX, phone)):
            if len(phone) == 12:
                self._value = f'+{phone}'
            elif len(phone) == 10:
                self._value = f'+38{phone}'
            elif len(phone) == 13:
                self._value = phone
        else:
            raise ValueError(f"Phone must be in format +380XXXXXXXXX/380XXXXXXXXX/0XXXXXXXXX")


class Email(Field):
    @Field.value.setter
    def value(self, email: str):
        if not isinstance(email, str):
            raise TypeError('Email must be a string')
        if not re.match(EMAIL_REGEX, email):
            raise ValueError('Email not valid')
        self._value = email


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        try:
            d, m, y = new_value.split('-')
            date = datetime(day=int(d), month=int(m), year=int(y))
            self._value = date
        except ValueError:
            print('Enter date like dd-mm-yyyy')


class Address(Field):
    @Field.value.setter
    def value(self, address: str):
        if not isinstance(address, str):
            raise TypeError('Address must be a string')
        if not re.match(ADDRESS_REGEX, address):
            raise ValueError('Address must be between 2 and 20 characters')
        self._value = address


class Record:
    def __init__(self, name: Name, phone: Phone, adr: Address, email: Email, birthday: Birthday = None):
        self.name = name
        self.address = adr
        self.email = email
        self.birthday = birthday
        self.phones = []
        if phone:
            self.add_address(phone)

    def add_address(self, adr: Phone):
        self.phones.append(adr)

    def add_birthday(self, birthday: Birthday):
        if birthday:
            self.birthday = birthday

    def __repr__(self):
        if self.birthday:
            return f'{", ".join([p.value for p in self.phones])} Birthday: {self.birthday.value.date()}\nAddress: {self.address.value}, Email: {self.email.value}'
        return f'{", ".join([p.value for p in self.phones])}\nAddress: {self.address.value}, Email: {self.email.value}'


class AddressBook(UserDict):
    def add_record(self, record: Record) -> Record | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            return record

    def __init__(self, *args):
        super().__init__(*args)
        self.load_data()

    def save_data(self):
        with open(ADDRESSBOOK_DB, 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        try:
            with open(ADDRESSBOOK_DB, 'rb') as f:
                try:
                    data = pickle.load(f)
                    self.data = data
                except EOFError:
                    return 'File data is empty'
        except FileNotFoundError:
            return 'File data is empty'

    def to_find(self, value):
        result = []
        for k, v in self.data.items():
            v = str(v)
            [result.append(f'{k.title()} {v}') for i in value if i in v]
        return print(f' Found {len(result)} records: \n{", ".join(result)}')

    def delete_record(self, name):
        if name in self:
            self.pop(name)
            return print(f"Record {name} was deleted")

        return print(f"Record {name} was not found")

    def update_record(self, old_value, new_value):
        new_value = str(new_value)
        for name, record in self.data.items():
            if name == old_value and name != new_value:
                self.data[new_value] = record
                self.data.pop(old_value)
                return print(f"Record {old_value} was updated to {new_value}")

            if old_value in str(record):
                list_records = []
                new_record = str(record).replace(old_value, new_value)
                self.data[name] = new_record
                return print(f"Record {record} was updated to {new_record}")

        return print(f"Record {old_value} was not found")


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Please enter the contact like this:\nName: number"
        except KeyError:
            return "This contact doesn't exist."
        except ValueError:
            return "Phone must contain only digits and be 10 symbols long"

    return inner


def to_help(*args):
    return """help - output command, that you can use to get help
    hello - output greeting message
    add - add new contact: like this: Name, Phone, Address, Email, Birthday
    show - show all contacts
    show phone - show number of contact"""


@input_error
def greeting(*args):
    return "How can I help you?"



@input_error
def to_exit(*args):
    notebook.save_data()
    return 'Goodbye!\nHave a nice day!'


notebook = AddressBook()


@input_error
def add_contact(*args):
    rec = Record(Name(args[0]), Phone(args[1]), Address(args[2]), Email(args[3]))
    notebook.add_record(rec)
    try:
        rec.add_birthday(Birthday(args[4]))
    except IndexError:
        birthday = None
    return f"Contact {rec.name.value} has added successfully."


@input_error
def print_phone(*args):
    return notebook[args[0]]


def show_all(*args):
    return "\n".join([f"{k.title()}: {v}" for k, v in notebook.items()]) if len(notebook) > 0 else 'Contacts are empty'


@input_error
def days_to_births(*args):
    num = 0
    try:
        num = int(args[0])
    except ValueError:
        print('Enter integer')
        return ''
    res = []
    for k, v in notebook.items():
        if v.birthday is None:
            continue
        date_now = datetime.now().date()
        birthday_date = datetime(day=v.birthday.value.day, month=v.birthday.value.month, year=date_now.year).date()
        if date_now > birthday_date:
            birthday_date = datetime(day=v.birthday.value.day, month=v.birthday.value.month,
                                     year=date_now.year + 1).date()
        result = birthday_date - date_now
        if result.days <= num:
            res.append(v)
    return "\n".join([f"{value.name.value.title()}: {value}" for value in res]) if len(
        res) > 0 else 'Contacts not found'


def find(*args):
    result_str = ''
    for i in notebook.to_find(args):
        result_str += f'{i}\n'
    return result_str[:-1] if result_str else 'Nothing found'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


all_commands = {
    greeting: ["hello", "hi"],
    add_contact: ["add", "new", "+"],
    #     change_number: ["change", ],
    print_phone: ["phone", "number"],
    show_all: ["show all", "show"],
    to_exit: ["good bye", "close", "exit", ".", "bye"],
    #     del_number: ["del", "delete", "-"],
    #     del_contact: ["remove", ],
    days_to_births: ["days", "birthday"],
    #     find: ["find", "search"],
    find: ["find", "search"],
    to_help: ["help", "?", "h"],
}


# def command_parser(user_input: str):
#     for key, value in all_commands.items():
#         print(key, value)
#         for i in value:
#             if user_input.lower().startswith(i.lower()):
#                 return key, user_input[len(i):].strip().split()
#     else:
#         return unknown_command, []


def main():
    print("Hi! Welcome to Personal Assistant Bot")
    show_menu()
    command = input("Write your command: ").casefold().strip()

    while command_handler(command):
        command = input("Write your command: ").casefold().strip()


# def main():
#     while True:
#         user_input = input('Please enter your command: ')
#         command, parser_data = command_parser(user_input)
#         print(command(*parser_data))
#         if command is to_exit:
#             break


if __name__ == "__main__":
    main()
