import pickle
from collections import UserDict
from datetime import datetime


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
    pass


class Phone(Field):
    pass


class Email(Field):
    pass


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
    pass

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


class AddressBook(UserDict):
    def add_record(self, record: Record) -> Record | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            return record

    def __init__(self, *args):
        super().__init__(*args)
        self.load_data()

    def save_data(self):
        with open('data.bin', 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        try:
            with open('data.bin', 'rb') as f:
                try:
                    data = pickle.load(f)
                    self.data = data
                except EOFError:
                    print('File data is empty')
        except FileNotFoundError:
            print('File data is empty')


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


@input_error
def greeting(*args):
    return "How can I help you?"


@input_error
def to_exit(*args):
    notebook.save_data()
    return 'Goodbye!'


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
        birthday_date = datetime(year=date_now.year, month=v.birthday.value.month, day=v.birthday.value.day).date()
        if date_now > birthday_date:
            birthday_date = datetime(year=date_now.year + 1, month=v.birthday.value.month,
                                     day=v.birthday.value.day).date()
        result = birthday_date - date_now
        if result.days <= num:
            res.append(v)
    return "\n".join([f"{value.name.value.title()}: {value}" for value in res]) if len(res) > 0 else 'Contacts not found'


all_commands = {
    greeting: ["hello", "hi"],
    add_contact: ["add", "new", "+"],
    #     change_number: ["change", ],
    #     print_phone: ["phone", "number"],
    show_all: ["show all", "show"],
    to_exit: ["good bye", "close", "exit", ".", "bye"],
    #     del_number: ["del", "delete", "-"],
    #     del_contact: ["remove", ],
    days_to_births: ["days", "birthday"],
    #     find: ["find", "search"],
}


def command_parser(user_input: str):
    for key, value in all_commands.items():
        for i in value:
            if user_input.lower().startswith(i.lower()):
                return key, user_input[len(i):].strip().split()


def main():
    while True:
        user_input = input(">>> ")
        command, parser_data = command_parser(user_input)
        print(command(*parser_data))
        if command is to_exit:
            break


if __name__ == "__main__":
    main()
