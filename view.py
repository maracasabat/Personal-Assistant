from pick import pick
from difflib import get_close_matches
from main import Record, AddressBook, Name, Phone, Address, Email, Birthday

notebook = AddressBook()
add_commands = ["add", "+", "new"]
exit_commands = ["exit", "bye", "goodbye", "close"]
update_commands = ["update", "change", "edit"]
back_to_menu_commands = ["menu", "quit", "back to menu", "back"]

commands = [f'{", ".join(add_commands)}', "show", "delete", "find", f'{", ".join(update_commands)}', "menu",
            "help", f'{", ".join(exit_commands)}']
description = ['Add contact', 'Show contacts', 'Delete Contact', 'Find Contact', 'Update Contact', 'Back to Menu',
               'Help', 'Exit Commands']
all_commands = commands + add_commands + exit_commands + update_commands + back_to_menu_commands


def show_edit_submenu():
    edit_options = ["Contact name", "Contact phone number", "contact address", "Contact email", "Contact birthday",
                    "Back"]
    option, index = pick(edit_options, f"Choose a field to update:\n{'=' * 60}", indicator="=>")
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")
    return index


def command_handler(command):
    if not isinstance(command, int):
        try:
            command = get_close_matches(command, all_commands, n=1, cutoff=0.5)[0]
            # print(all_commands)
            print(f'You have chosen a command: {command}')
        except IndexError:
            print("Sorry, I don't understand. Please try again.")
            return True
    if command == "help" or command == 6:
        show_submenu()
        # return command_handler(show_commands())
    if command == "add" or command == 0:
        try:
            name = input("Enter name: ").title().strip()
            phone_number = input("Enter phone-number: ").strip()
            address = input("Enter address: ").strip()
            email = input("Enter email: ").strip()
            birthday = input("Enter birthday dd-mm-yyyy: ").strip()
            record = Record(Name(name), Phone(phone_number), Address(address), Email(email), Birthday(birthday))
            notebook.add_record(record)
            notebook.save_data()
            return True
        except ValueError as e:
            print(f"Sorry, {e}. Please try again.")
            return True
    if command == "show" or command == 1:
        print(notebook)
        return True
    if command == "delete" or command == 2:
        name = input("Enter name: ").title().strip()
        notebook.delete_record(name)
        notebook.save_data()
        return True
    if command == "find" or command == 3:
        value = input("Enter name/phone/birthday for find: ")
        notebook.to_find(value)
        return True
    if command in update_commands or command == 4:
        updated_position = show_edit_submenu()
        if updated_position == 0:
            old_value = input("Enter old name: ").title()
            new_value = input("Enter new name: ").title()
            notebook.update_record(old_value, new_value)
            notebook.save_data()
            return True
        elif updated_position == 1:
            old_value = input("Enter old phone-number: ")
            new_value = input("Enter new phone-number: ")
            notebook.update_record(old_value, Phone(new_value))
            return True
        elif updated_position == 2:
            old_value = input("Enter old address: ").strip()
            new_value = input("Enter new address: ").strip()
            notebook.update_record(old_value, Address(new_value))
            notebook.save_data()
            return True
        elif updated_position == 3:
            old_value = input("Enter old email: ").strip()
            new_value = input("Enter new email: ").strip()
            notebook.update_record(old_value, Email(new_value))
            return True
        elif updated_position == 4:
            old_value = input("Enter old birthday: ")
            new_value = input("Enter new birthday: ")
            notebook.update_record(old_value, new_value)
            return True
        elif updated_position == 5:
            notebook.save_data()
            return True
        else:
            print("Wrong command")
            return True

    if command in back_to_menu_commands or command == 5:
        show_menu()
        return True
    if command in exit_commands or command == 7:
        print("Goodbye!")
        notebook.save_data()
        return False
    else:
        print("Unknown command")


submenu_options = [f"{cmd:<20} -  {desc}" for cmd, desc in zip(commands, description)]
submenu_title = f"Command name and description. Select command.\n{'=' * 46}"


def show_submenu():
    option, index = pick(submenu_options, submenu_title, indicator="=>")
    option = option.split(" - ")[1]
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")

    return submenu_switcher(index)


def submenu_switcher(index):
    return command_handler(index)


menu_title = f"Hi! Welcome to personal assistant bot!\nSelect menu option please.\n{'=' * 60}".upper()
menu_options = ["AddressBook", "NoteBook", "Help", "Exit"]


def show_menu():
    option, index = pick(menu_options, menu_title, indicator="=>")
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")

    return menu_switcher(index)


def menu_switcher(index):
    if index == 0:
        print("welcome to Addressbook")
        notebook.load_data()
        command = input("Write your command: ").casefold().strip()
        while command_handler(command):
            command = input("Write your command: ").casefold().strip()

    if index == 1:
        print("Welcome to Notebook")
        notebook.load_data()
        command = input("Write your command: ").casefold().strip()
        while command_handler(command):
            command = input("Write your command: ").casefold().strip()
    if index == 2:
        show_submenu()

    if index == 3:
        print("See you later!")
        notebook.save_data()
