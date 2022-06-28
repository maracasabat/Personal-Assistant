from Personal_assistant.classes import SomeBook, Record, Name, Phone, Address, Email, Birthday
from datetime import datetime

addressbook = SomeBook('data.bin')


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
def days_to_birthday(*args):
    num = 0
    try:
        num = int(args[0])
    except ValueError:
        print('Enter integer')
        return ''
    res = []
    for k, v in addressbook.items():
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
    return print("\n".join([f"{value.name.value.title()}: {value}" for value in res]) if len(
        res) > 0 else 'Contacts not found')


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
    show phone - show number of contact
    days n - where n is integer, show contacts who have a birthday next n day"""


@input_error
def greeting(*args):
    return "How can I help you?"


@input_error
def to_exit(*args):
    addressbook.save_data()
    return 'Goodbye!\nHave a nice day!'


@input_error
def add_contact(*args):
    rec = Record(Name(args[0]), Phone(args[1]), Address(args[2]), Email(args[3]))
    addressbook.add_record(rec)
    try:
        rec.add_birthday(Birthday(args[4]))
    except IndexError:
        birthday = None
    return f"Contact {rec.name.value} has added successfully."


@input_error
def print_phone(*args):
    return addressbook[args[0]]


@input_error
def show_all(*args):
    return "\n".join([f"{k.title()}: {v}" for k, v in addressbook.items()]) if len(
        addressbook) > 0 else 'Contacts are empty'


def find(*args):
    result_str = ''
    for i in addressbook.to_find(args):
        result_str += f'{i}\n'
    return result_str[:-1] if result_str else 'Nothing found'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


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
    show phone - show number of contact
    days n - where n is integer, show contacts who have a birthday next n day"""


@input_error
def greeting(*args):
    return "How can I help you?"


@input_error
def to_exit(*args):
    addressbook.save_data()
    return 'Goodbye!\nHave a nice day!'


@input_error
def add_contact(*args):
    rec = Record(Name(args[0]), Phone(args[1]), Address(args[2]), Email(args[3]))
    addressbook.add_record(rec)
    try:
        rec.add_birthday(Birthday(args[4]))
    except IndexError:
        birthday = None
    return f"Contact {rec.name.value} has added successfully."


@input_error
def print_phone(*args):
    return addressbook[args[0]]


@input_error
def show_all(*args):
    return "\n".join([f"{k.title()}: {v}" for k, v in addressbook.items()]) if len(
        addressbook) > 0 else 'Contacts are empty'


def find(*args):
    result_str = ''
    for i in addressbook.to_find(args):
        result_str += f'{i}\n'
    return result_str[:-1] if result_str else 'Nothing found'


def unknown_command(*args):
    return 'Unknown command! Enter again!'
