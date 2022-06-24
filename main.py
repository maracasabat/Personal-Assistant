from collections import UserDict


class Field:
    pass


class Name(Field):
    pass


class Phone(Field):
    pass


class Email(Field):
    pass


class Birthday(Field):
    pass


class Record:
    pass


class AddressBook(UserDict):
    pass


def greeting(*args):
    return "How can I help you?"


def to_exit(*args):
    return 'Goodbye!'


all_commands = {

    greeting: ["hello", "hi"],
    #     add_contact: ["add", "new", "+"],
    #     change_number: ["change", ],
    #     print_phone: ["phone", "number"],
    #     show_all: ["show all", "show"],
    to_exit: ["good bye", "close", "exit", ".", "bye"],
    #     del_number: ["del", "delete", "-"],
    #     del_contact: ["remove", ],
    #     days_to_births: ["days", "birthday"],
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
