from pick import pick
import os
from difflib import get_close_matches
from Personal_assistant.helpers import days_to_birthday
# from Personal_assistant.sorter import start
from styles import show_records, show_notes, show_print, bcolors, pretty_title
from classes import Record, SomeBook, Name, Phone, Address, Email, Birthday, NoteBookRecord, NoteBookText, NoteBookTeg

addressbook = SomeBook('data.bin')
notebook = SomeBook('notebook_data.bin')
add_commands = ["add", "+", "new"]
exit_commands = ["exit", "bye", "goodbye", "close"]
days_to_birthday_commands = ["days to", "birthday", "period"]
update_commands = ["update", "change", "edit"]
back_to_menu_commands = ["menu", "quit", "back to menu", "back"]

contact_commands = [f'{", ".join(add_commands)}', "show", "delete", "find", f'{", ".join(days_to_birthday_commands)}',
                    f'{", ".join(update_commands)}', "menu", "help", f'{", ".join(exit_commands)}']
all_commands = contact_commands + add_commands + exit_commands + update_commands + back_to_menu_commands + days_to_birthday_commands

contact_description = ['Add contact', 'Show contacts', 'Delete contact', 'Find contact', 'Show contacts birthday',
                       'Update contact', 'Back to Menu', 'Help', 'Exit commands']

# ======================== Menu & Submenu options ========================
menu_title = f"Hi! Welcome to personal assistant bot!\nSelect menu option please.\n{'=' * 60}".upper()
menu_options = ["AddressBook", "NoteBook", "Help", "Folder Sorter ", "Exit"]

contact_submenu_options = [f"{cmd:<30} -  {desc}" for cmd, desc in zip(contact_commands, contact_description)]
contact_submenu_title = f"Command name and description. Select command.\n{'=' * 60}"

notes_commands = [f'{", ".join(add_commands)}', "show", "delete", "find", 'sort',
                  f'{", ".join(update_commands)}', "menu", "help", f'{", ".join(exit_commands)}']
notes_description = ['Add Note', 'Show Notes', 'Delete Note', 'Find Note', 'Sort Notes',
                     'Update Note', 'Back to Menu', 'Help', 'Exit commands']

notes_submenu_options = [f"{cmd:<30} -  {desc}" for cmd, desc in zip(notes_commands, notes_description)]
notes_submenu_title = f"Command name and description. Select command.\n{'=' * 60}"

help_submenu_options = [f"{cmd:<30} -  {desc}" for cmd, desc in
                        zip(['Contacts', 'Notes'], ['Addressbook Help Commands', 'Notes Help Commands'])]
help_submenu_title = f"Command name and description. Select command.\n{'=' * 60}"


# ============================= Main Menu =================+++++++=================================
def show_menu():
    option, index = pick(menu_options, menu_title, indicator="=>")
    print(
        f"{bcolors.OKGREEN}You have chosen a command: {bcolors.HEADER}{option}{bcolors.ENDC}.{bcolors.OKGREEN}\nLet's continue.\n{'=' * 60}{bcolors.ENDC}")

    return menu_switcher(index)


def menu_switcher(index):
    if index == 0:
        os.system('clear')
        pretty_title(f"Welcome to Addressbook.\n{'=' * 60}")
        addressbook.load_data()
        show_contacts_submenu()
        command = input("Write your command: ").casefold().strip()
        while contacts_handler(command):
            command = input("Write your command: ").casefold().strip()

    if index == 1:
        os.system('clear')
        pretty_title(f"Welcome to Notebook.\n{'=' * 60}")
        notebook.load_data()
        show_notes_submenu()
        command = input("Write your command: ").casefold().strip()
        while notes_handler(command):
            command = input("Write your command: ").casefold().strip()

    if index == 2:
        show_help_submenu()
    if index == 3:
        pretty_title(f"Welcome to Folder Sorter.\n{'=' * 60}")
        path = input("Enter path to folder: ")
        # start()  # start folder sorter
    if index == 4:
        print(f"{bcolors.HEADER}See you later!{bcolors.ENDC}")
        addressbook.save_data()
        notebook.save_data()


# ============================= Contacts SubMenu ==================================================

def show_contacts_submenu():
    option, index = pick(contact_submenu_options, contact_submenu_title, indicator="=>")
    option = option.split(" - ")[1]
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")

    return contacts_submenu_switcher(index)


def contacts_submenu_switcher(index):
    return contacts_handler(index)


def show_edit_contact_submenu():
    edit_options = ["Contact name", "Contact phone number", "contact address", "Contact email", "Contact birthday",
                    "Back"]
    option, index = pick(edit_options, f"Choose a field to update:\n{'=' * 60}", indicator="=>")
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")
    return index


# ============================= C Notes  SubMenu ==================================================

def show_edit_note_submenu():
    edit_options = ["Note title", "Note text", "Add note tag", "Del note tag", "Back"]
    option, index = pick(edit_options, f"Choose a field to update:\n{'=' * 60}", indicator="=>")
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")
    return index


def show_notes_submenu():
    option, index = pick(notes_submenu_options, notes_submenu_title, indicator="=>")
    option = option.split(" - ")[1]
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")

    return notes_submenu_switcher(index)


def notes_submenu_switcher(index):
    return notes_handler(index)


# ============================= Contacts and Notes  HELP SubMenu ==================================================

def show_help_submenu():
    option, index = pick(help_submenu_options, help_submenu_title, indicator="=>")
    option = option.split(" - ")[1]
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")

    return help_submenu_switcher(index)


def help_submenu_switcher(index):
    if index == 0:
        return show_contacts_submenu()
    if index == 1:
        return show_notes_submenu()
    else:
        print(f"{bcolors.WARNING}Unknown command{bcolors.ENDC}")
        return show_help_submenu()


# ============================= Contact Menu and Notes Menu handlers ===============================================

def contacts_handler(command):
    if not isinstance(command, int):
        try:
            os.system('clear')
            command = get_close_matches(command, all_commands, n=1, cutoff=0.4)[0]
            print(f'{bcolors.OKGREEN}You have chosen a command: {bcolors.HEADER}{command}{bcolors.ENDC}')
        except IndexError:
            print(f"{bcolors.WARNING}Sorry, I don't understand. Please try again.{bcolors.ENDC}")
            return True
    if command == "add" or command == 0:
        try:
            os.system('clear')
            pretty_title(f"Add contact please: \n{'=' * 40}")
            name = input("Enter name: ").title().strip()
            phone_number = input("Enter phone-number: ").strip()
            address = input("Enter address: ").strip()
            email = input("Enter email: ").strip()
            birthday = input("Enter birthday dd-mm-yyyy: ").strip()
            record = Record(Name(name), Phone(phone_number), Address(address), Email(email))
            record.add_birthday(Birthday(birthday))
            addressbook.add_record(record)
            addressbook.save_data()
            return True
        except ValueError as e:
            print(f"{bcolors.FAIL}Sorry, {e}. Please try again.{bcolors.ENDC}")
            return True
    if command == "show" or command == 1:
        show_records(addressbook)
        return True
    if command == "delete" or command == 2:
        name = input("Enter name: ").title().strip()
        addressbook.delete_record(name)
        addressbook.save_data()
        return True
    if command == "find" or command == 3:
        value = input("Enter contact name: ")
        addressbook.to_find(value)
        return True
    if command in days_to_birthday_commands or command == 4:
        period = input("Enter days to birthday: ")
        print(f"Days to birthday {period}")
        days_to_birthday(period)
        return True
    if command in update_commands or command == 5:
        updated_position = show_edit_contact_submenu()
        if updated_position == 0:
            old_value = input("Enter old name: ").title()
            new_value = input("Enter new name: ").title()
            addressbook.update_record(old_value, new_value)
            addressbook.save_data()
            return True
        elif updated_position == 1:
            old_value = input("Enter old phone-number: ")
            new_value = input("Enter new phone-number: ")
            addressbook.update_record(old_value, Phone(new_value))
            return True
        elif updated_position == 2:
            old_value = input("Enter old address: ").strip()
            new_value = input("Enter new address: ").strip()
            addressbook.update_record(old_value, Address(new_value))
            addressbook.save_data()
            return True
        elif updated_position == 3:
            old_value = input("Enter old email: ").strip()
            new_value = input("Enter new email: ").strip()
            addressbook.update_record(old_value, Email(new_value))
            return True
        elif updated_position == 4:
            old_value = input("Enter old birthday: ")
            new_value = input("Enter new birthday: ")
            addressbook.update_record(old_value, new_value)
            return True
        elif updated_position == 5:
            addressbook.save_data()
            return True
        else:
            print("Wrong command")
            return True
    if command in back_to_menu_commands or command == 6:
        show_menu()
        return True
    if command == "help" or command == 7:
        show_contacts_submenu()
        return True
    if command in exit_commands or command == 8:
        print("Goodbye!")
        addressbook.save_data()
        return False
    else:
        print(f"{bcolors.WARNING}Unknown command{bcolors.ENDC}")


def notes_handler(command):
    if not isinstance(command, int):
        try:
            os.system('clear')
            command = get_close_matches(command, all_commands, n=1, cutoff=0.5)[0]
            print(f'{bcolors.OKGREEN}You have chosen a command: {bcolors.HEADER}{command}{bcolors.ENDC}')
        except IndexError:
            print(f"{bcolors.WARNING}Sorry, I don't understand. Please try again.{bcolors.ENDC}")
            return True
    if command == "add" or command == 0:
        try:
            os.system('clear')
            pretty_title(f"Add a note please:\n{'=' * 40}")
            title = input("Enter title: ").title().strip()
            text = input("Enter text: ").strip()
            teg = input("Enter tag like teg1, teg2: ").strip()
            show_print(f'{title}; {text}; {teg}')
            note = NoteBookRecord(Name(title), NoteBookText(text))
            tegs_list = teg.split(',')
            for tg in tegs_list:
                note.add_teg(NoteBookTeg(tg.strip()))
            notebook.add_record(note)
            notebook.save_data()
            return True
        except ValueError as e:
            print(f"{bcolors.FAIL}Sorry, {e}. Please try again.{bcolors.ENDC}")
            return True
    if command == "show" or command == 1:
        show_notes(notebook)
        return True
    if command == "delete" or command == 2:
        title = input("Enter title: ").title().strip()
        notebook.delete_record(title)
        notebook.save_data()
        return True
    if command == "find" or command == 3:
        value = input("Enter value for find: ").strip()
        result_str = ''
        for k, v in notebook.items():
            found = False
            if value.title() in k.title():
                found = True
            text = v.text.value.upper()
            if text.find(value.upper()) != -1:
                found = True
            else:
                for teg in v.tegs:
                    tg = teg.value.upper()
                    if tg.find(value.upper()) != -1:
                        found = True
            if found:
                result_str += f'{v}'
        show_print(result_str) if result_str else f'{bcolors.WARNING}Nothing was found!{bcolors.ENDC}'
        return True
    if command == "sort" or command == 4:
        value = input("Enter value for sort: ").strip()
        print(f"Sort by {value}")  # дописать сортировку  notes
        return True
    if command in update_commands or command == 5:
        updated_position = show_edit_note_submenu()
        if updated_position == 0:
            old_title = input("Enter old title: ").title().strip()
            new_title = input("Enter new title: ").title().strip()
            new_value = str(new_title)
            for name, record in notebook.data.items():
                if name == old_title:
                    record.name.value = new_value
                    notebook.pop(old_title)
                    notebook[new_value] = record
                    print(f"Record {old_title} was updated to {new_value}")
                    return True
            notebook.save_data()
            return True
        if updated_position == 1:
            name = input("Enter name: ").title().strip()
            new_text = input("Enter new text: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.text = NoteBookText(new_text)
            else:
                print(f'Note title {name} is nit found')
            notebook.save_data()
            return True
        if updated_position == 2:
            name = input("Enter name: ").title().strip()
            new_teg = input("Enter new tag: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.add_teg(NoteBookTeg(new_teg))
            notebook.save_data()
            return True
        if updated_position == 3:
            name = input("Enter name: ").title().strip()
            new_teg = input("Enter del tag: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.del_teg(new_teg)
            notebook.save_data()
            return True
    if command in back_to_menu_commands or command == 6:
        show_menu()
        return True
    if command == "help" or command == 7:
        show_notes_submenu()
        return True
    if command in exit_commands or command == 8:
        print("Goodbye!")
        notebook.save_data()
        return False
    else:
        print(f"{bcolors.WARNING}Unknown command{bcolors.ENDC}")
