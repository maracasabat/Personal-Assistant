from main import *
from pick import pick
from difflib import get_close_matches

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
    if command in add_commands or command == 0:
        name = input("Enter name: ")
        phone_number = input("Enter phone-number: ")
        address = input("Enter address: ")
        email = input("Enter email: ")
        birthday = input("Enter birthday 00-00-0000: ")
        record = Record(Name(name), Phone(phone_number), Address(address), Email(email), Birthday(birthday))
        notebook.add_record(record)
        notebook.save_data()
        return True
    if command == "show" or command == 1:
        print(notebook)
        return True
    if command == "delete" or command == 2:
        name = input("Enter name: ")
        notebook.delete_record(name)
        notebook.save_data()
        return True
    if command == "find" or command == 3:
        value = input("Enter name/phone/birthday for find: ")
        notebook.find(value)
        return True
    if command in update_commands or command == 4:
        updated_position = input('Enter for update: name - 1, phone number - 2, address - 3, email - 4, birthday - 5: ')
        try:
            updated_position = int(updated_position)
        except ValueError:
            print("Sorry, I don't understand. Please try again.")
            return True
        if updated_position == 1:
            old_value = input("Enter old name: ").title()
            new_value = input("Enter new name: ").title()
            notebook.update_record(old_value, new_value)
            return True
        elif updated_position == 2:
            old_value = input("Enter old phone-number: ")
            new_value = input("Enter new phone-number: ")
            notebook.update_record(old_value, new_value)
            return True
        elif updated_position == 3:
            old_value = input("Enter old address: ")
            new_value = input("Enter new address: ")
            notebook.update_record(old_value, new_value)
            return True
        elif updated_position == 4:
            old_value = input("Enter old email: ")
            new_value = input("Enter new email: ")
            notebook.update_record(old_value, new_value)
            return True
        elif updated_position == 5:
            old_value = input("Enter old birthday: ")
            new_value = input("Enter new birthday: ")
            notebook.update_record(old_value, new_value)
            return True
        else:
            print("Wrong command")
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
