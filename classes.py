import pickle
from collections import UserDict
from datetime import datetime
import re


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


class Name(Field):
    @Field.value.setter
    def value(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not re.match(r'^[a-zA-Zа-яА-Я]{2,20}$', name):
            raise ValueError('Name must be between 2 and 20 characters')
        self._value = name


class Phone(Field):
    @Field.value.setter
    def value(self, phone: str):
        if not isinstance(phone, str):
            raise TypeError('Phone must be a string')
        if not re.match(r'^\+380\d{3}\d{2}\d{2}\d{2}$', phone):
            raise ValueError('Phone must be in format +380XXXXXXXXX')
        self._value = phone


class Email(Field):
    @Field.value.setter
    def value(self, email: str):
        if not isinstance(email, str):
            raise TypeError('Emain must be a string')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise ValueError('Email must be in format')
        self._value = email


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value):
        try:
            d, m, y = new_value.split('-')
            date = datetime(day=int(d), month=int(m), year=int(y))
            self._value = date
        except ValueError:
            print('Enter date like 02-05-2022')


class Address(Field):
    @Field.value.setter
    def value(self, address: str):
        if not isinstance(address, str):
            raise TypeError('Address must be a string')
        if not re.match(r'^[a-zA-Zа-яА-Я0-9,. ]{2,20}$', address):
            raise ValueError('Address must be between 2 and 20 characters')
        self._value = address


class NoteBookText(Field):
    pass


class NoteBookTeg(Field):
    pass


class NoteBookRecord:
    def __init__(self, name: Name, text: NoteBookText):
        self.name = name
        self.text = text
        self.tegs = []

    def __repr__(self):
        return f'{self.name.value.title()}: {", ".join([p.value for p in self.tegs])}\nText:{self.text.value}'

    def add_teg(self, teg: NoteBookTeg):
        self.tegs.append(teg)

    def del_teg(self, teg: str):
        for i, tg in enumerate(self.tegs):
            if tg.value == teg:
                return self.tegs.pop(i)



class Record:
    def __init__(self, name: Name, phone: Phone, adr: Address, email: Email):
        self.name = name
        self.address = adr
        self.email = email
        self.birthday = None
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


class SomeBook(UserDict):

    def add_record(self, record: Record) -> Record | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
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

    def to_find(self, value):
        result = []
        for k, v in self.data.items():
            v = str(v)
            [result.append(f'{k.title()} {v}') for i in value if i in v]
        return result

