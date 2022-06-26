from classes import SomeBook, NoteBookRecord, NoteBookText, NoteBookTeg, Name

notebook = SomeBook('notebook_data.bin')

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Please enter the contact like this:\nName: text"
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
    return 'Goodbye!\nHave a nice day!'


@input_error
def add_note(*args):
    rec = NoteBookRecord(Name(args[0]), NoteBookText(args[1]))
    notebook.add_record(rec)
    return f"Note {rec.name.value} has added successfully."


@input_error
def print_text(*args):
    return notebook[args[0]]


@input_error
def show_all(*args):
    return "\n".join([f"{v}" for k, v in notebook.items()]) if len(
        notebook) > 0 else 'Contacts are empty'


@input_error
def del_note(*args):
    return notebook.pop(args[0])


@input_error
def set_teg(*args):
    note = notebook.get(args[0], None)
    if not note is None:
        note.add_teg(NoteBookTeg(args[1]))
        return f'Teg {args[1]} set'


@input_error
def del_teg(*args):
    note = notebook.get(args[0], None)
    if not note is None:
        note.del_teg(args[1])
        return f'Teg {args[1]} removed'


@input_error
def edit_text(*args):
    note = notebook.get(args[0], None)
    if not note is None:
        note.text = NoteBookText(args[1])
        return f'Teg {args[1]} changed'


@input_error
def find(*args):
    result_str = ''
    for k, v in notebook.items():
        found = False
        if args[0] in k:
            found = True
        elif args[0] in v.text.value:
            found = True
        elif args[0] in v.tegs:
            found = True
        if found:
            result_str += f'{v}\n'
    return result_str[:-1] if result_str else 'Nothing found'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


all_commands = {
    greeting: ["hello", "hi"],
    add_note: ["add", "new", "+"],
    #     change_number: ["change", ],
    print_text: ["text"],
    show_all: ["show all", "show"],
    to_exit: ["good bye", "close", "exit", ".", "bye"],
    del_teg: ["del", "delete", "-"],
    set_teg: ["set"],
    del_note: ["remove", ],
    edit_text: ['edit'],
    # days_to_births: ["days", "birthday"],
    #     find: ["find", "search"],
    find: ["find", "search"],
    # to_help: ["help", "?", "h"],
}


def command_parser(user_input: str):
    for key, value in all_commands.items():
        for i in value:
            if user_input.lower().startswith(i.lower()):
                return key, user_input[len(i):].strip().split(':')
    else:
        return unknown_command, []


def main():
    while True:
        user_input = input('Please enter your command: ')
        command, parser_data = command_parser(user_input)
        print(command(*parser_data))
        if command is to_exit:
            break


if __name__ == "__main__":
    main()