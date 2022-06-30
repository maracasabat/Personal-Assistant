import pickle
from collections import UserDict
from datetime import datetime
import re

from Personal_assistant.styles import bcolors

PHONE_REGEX = re.compile(r"^\+?(\d{2})?\(?(0\d{2})\)?(\d{7}$)")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
NAME_REGEX = re.compile(r'^[a-zA-Zа-яА-Я0-9,. ]{2,50}$')
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
            raise ValueError('Name must be between 2 and 50 characters')
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
            self._value = date.date()
        except ValueError:
            print('Enter date like dd-mm-yyyy')


class Address(Field):
    @Field.value.setter
    def value(self, address: str):
        if not isinstance(address, str):
             raise TypeError('Address must be a string')
        # if not re.match(ADDRESS_REGEX, address):
        #     raise ValueError('Address must be between 2 and 20 characters')
        self._value = address


class NoteBookText(Field):
    pass


class NoteBookTeg(Field):
    pass


class NoteBookRecord:
    def __init__(self, name: Name, text: NoteBookText, *args):
        self.name = name
        self.text = text
        self.tegs = []

    def __repr__(self):
        return f'{self.name.value.title()}; {", ".join([p.value for p in self.tegs])}; {self.text.value}'

    def add_teg(self, teg: NoteBookTeg):
        self.tegs.append(teg)

    def del_teg(self, teg: str):
        for i, tg in enumerate(self.tegs):
            if tg.value.upper() == teg.upper():
                return self.tegs.pop(i)


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
        new_str = f'{", ".join([p.value for p in self.phones])},'
        if self.email:
            new_str += f' {self.email.value},'
        else:
            new_str += f' {None},'
        if self.address:
            new_str += f' {self.address.value},'
        else:
            new_str += f' {None},'
        if self.birthday:
            new_str += f' {self.birthday.value}'
        else:
            new_str += f' {None}'
        return new_str


class SomeBook(UserDict):

    def add_record(self, record: Record) -> Record | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            self.save_data()
            return record

    def __init__(self, save_file, *args):
        super().__init__(*args)
        self.save_file = save_file
        self.load_data()

    def save_data(self):
        with open(self.save_file, 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        try:
            with open(self.save_file, 'rb') as f:
                try:
                    data = pickle.load(f)
                    self.data = data
                except EOFError:
                    return 'File data is empty'
        except FileNotFoundError:
            return 'File data is empty'

    def to_find(self, name):
        for k, v in self.data.items():
            if k.title() == name.title():
                return print(f'{k.title()} {v}')
        return print('Not found')

    def delete_record(self, name):
        if name in self:
            self.pop(name)
            return print(f"{bcolors.OKGREEN}Record {name} was  deleted successfully!{bcolors.ENDC}")

        return print(f"{bcolors.WARNING}Record {bcolors.HEADER}{name}{bcolors.WARNING} was not found! Please try again. {bcolors.ENDC}")

    def update_record(self, old_value, new_value):
        new_value = str(new_value)
        for name, record in self.data.items():
            if name == old_value and name != new_value:
                self.data[new_value] = record
                self.data.pop(old_value)
                return print(f"Record {old_value} was updated to {new_value}")

            if old_value in str(record):
                # list_records = []
                new_record = str(record).replace(old_value, new_value)
                self.data[name] = new_record
                return print(f"Record {record} was updated to {new_record}")

        return print(f"Record {old_value} was not found")