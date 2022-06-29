import sys
from pick import pick
import os
from difflib import get_close_matches
from sorter import start
from styles import show_records, show_notes, show_print, bcolors, pretty_title
from classes import Record, SomeBook, Name, Phone, Address, Email, Birthday, NoteBookRecord, NoteBookText, NoteBookTeg
from datetime import datetime

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

sorter_submenu_options = [f"{cmd:<30} -  {desc}" for cmd, desc in
                          zip(['File sorter', 'Back to menu'],
                              ['Please choose a folder to sort', 'Exit to the main menu'])]
sorter_submenu_title = f"Command name and description. Select command.\n{'=' * 60}"


# ================================ Menu Sorter ======================================================
def show_sorter_submenu():
    option, index = pick(sorter_submenu_options, sorter_submenu_title, indicator="=>")
    option = option.split(" - ")[1]
    print(f"You have chosen a command: {option}.\nLet's continue.\n{'=' * 60}")

    return sorter_submenu_switcher(index)


def sorter_submenu_switcher(index):
    return sorter_handler(index)


def sorter_handler(index):
    if index == 0:
        start()
        print('For sorted files, please choose a folder to sort.')
    if index == 1:
        show_menu()
        print('Back to menu')


# ============================= Main Menu =================+++++++=================================
def show_menu():
    option, index = pick(menu_options, menu_title, indicator="=>")
    print(
        f"{bcolors.OKGREEN}You have chosen a command: {bcolors.HEADER}{option}{bcolors.ENDC}.{bcolors.OKGREEN}\nLet's continue.\n{'=' * 60}{bcolors.ENDC}")

    return menu_switcher(index)


def menu_switcher(index):
    if index == 0:
        os.system('clear') | os.system('cls')
        pretty_title(f"Welcome to Addressbook.\n{'=' * 60}")
        addressbook.load_data()
        show_contacts_submenu()
        command = input("Write your command: ").casefold().strip()
        while contacts_handler(command):
            command = input("Write your command: ").casefold().strip()

    if index == 1:
        os.system('clear') | os.system('cls')
        pretty_title(f"Welcome to Notebook.\n{'=' * 60}")
        notebook.load_data()
        show_notes_submenu()
        command = input("Write your command: ").casefold().strip()
        while notes_handler(command):
            command = input("Write your command: ").casefold().strip()

    if index == 2:
        show_help_submenu()
    if index == 3:
        os.system('clear') | os.system('cls')
        pretty_title(f"Welcome to Folder Sorter.\n{'=' * 60}")
        show_sorter_submenu()
        command = input("Write your command: ").casefold().strip()
        if command in back_to_menu_commands:
            show_menu()
        else:
            while sorter_handler(command):
                command = input("Write your command: ").casefold().strip()
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
            os.system('clear') | os.system('cls')
            command = get_close_matches(command, all_commands, n=1, cutoff=0.4)[0]
            print(f'{bcolors.OKGREEN}You have chosen a command: {bcolors.HEADER}{command}{bcolors.ENDC}')
        except IndexError:
            print(f"{bcolors.WARNING}Sorry, I don't understand. Please try again.{bcolors.ENDC}")
            return True
    if command == "add" or command == 0:
        try:
            os.system('clear') | os.system('cls')
            pretty_title(f"Add contact please: \n{'=' * 40}")
            name = input("Enter name: ").title().strip()
            phone_number = input("Enter phone-number: ").strip()
            address = input("Enter address: ").strip()
            email = input("Enter email: ").strip()
            birthday = input("Enter birthday dd-mm-yyyy: ").strip()
            address_new = None
            if address:
                address_new = Address(address)
            email_new = None
            if email:
                email_new = Email(email)
            record = Record(Name(name), Phone(phone_number), address_new, email_new)
            if birthday:
                record.add_birthday(Birthday(birthday))
            addressbook.add_record(record)
            print(f"{bcolors.OKGREEN}Contact added successfully{bcolors.ENDC}")
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
        print(f"{bcolors.OKGREEN}Days to birthday: {bcolors.HEADER}{period}{bcolors.ENDC}")
        num = 0
        try:
            num = int(period)
        except ValueError:
            print(f'{bcolors.WARNING}Enter integer{bcolors.ENDC}')
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
        print("\n".join([f"{value.name.value.title()}: {value}" for value in res]) if len(
            res) > 0 else f'{bcolors.WARNING}Contacts not found!{bcolors.ENDC}')
        return True
    if command in update_commands or command == 5:
        updated_position = show_edit_contact_submenu()
        if updated_position == 0:
            old_value = input("Enter old name: ").title()
            new_value = input("Enter new name: ").title()
            for name, record in addressbook.data.items():
                if name == old_value:
                    record.name.value = new_value
                    addressbook.pop(old_value)
                    addressbook[new_value] = record
                    print(f"{bcolors.OKGREEN}Record {bcolors.HEADER}{old_value}{bcolors.OKGREEN} was updated to {bcolors.HEADER} {new_value}{bcolors.ENDC}")
                    return True
            print(f"{bcolors.WARNING}Record {bcolors.HEADER}{old_value}{bcolors.WARNING} was not found{bcolors.ENDC}")
            addressbook.save_data()
            return True
        elif updated_position == 1:
            name = input("Enter name: ").title().strip()
            new_value = input("Enter new phone-number: ")
            record = addressbook.get(name, -1)
            if record != -1:
                if len(record.phones) >= 1:
                    record.phones[0] = Phone(new_value)
                    print(f"{bcolors.OKGREEN}Phone number was updated!{bcolors.ENDC}")
                else:
                    record.phones.append(Phone(new_value))
                    print(f"{bcolors.OKGREEN}Phone number was updated!{bcolors.ENDC}")
            else:
                print(f'{bcolors.WARNING}Contact name {bcolors.HEADER}{name}{bcolors.WARNING} was not found!{bcolors.ENDC}')
            addressbook.save_data()
            return True
        elif updated_position == 2:
            name = input("Enter name: ").title().strip()
            new_value = input("Enter new address: ").strip()
            record = addressbook.get(name, -1)
            if record != -1:
                record.address = Address(new_value)
                print(f"{bcolors.OKGREEN}Contact address was updated to: {bcolors.HEADER}{new_value}{bcolors.ENDC}")
            else:
                print(f'{bcolors.WARNING}Contact {bcolors.HEADER}{name}{bcolors.OKGREEN} was not found!{bcolors.ENDC}')
            addressbook.save_data()
            return True
        elif updated_position == 3:
            name = input("Enter name: ").title().strip()
            new_value = input("Enter new email: ").strip()
            record = addressbook.get(name, -1)
            if record != -1:
                record.email = Email(new_value)
                print(f"{bcolors.OKGREEN}Contact email was updated to: {bcolors.HEADER} {new_value}{bcolors.ENDC}")
            else:
                print(f'{bcolors.WARNING}Contact {bcolors.HEADER}{name}{bcolors.WARNING} was not found{bcolors.ENDC}!')
            addressbook.save_data()
            return True
        elif updated_position == 4:
            name = input("Enter name: ").title().strip()
            new_value = input("Enter new birthday: ")
            record = addressbook.get(name, -1)
            if record != -1:
                record.birthday = Birthday(new_value)
                print(f"{bcolors.OKGREEN}Birthday {bcolors.HEADER}{new_value}{bcolors.OKGREEN} was added to {bcolors.HEADER}{name}{bcolors.ENDC}")
            else:
                print(f'{bcolors.WARNING}Contact {bcolors.HEADER}{name}{bcolors.WARNING} was not found{bcolors.ENDC}!')
            addressbook.save_data()
            return True
        elif updated_position == 5:
            show_contacts_submenu()
            addressbook.save_data()
            return True
        else:
            print(f"{bcolors.WARNING}Wrong command{bcolors.ENDC}!")
            return True
    if command in back_to_menu_commands or command == 6:
        show_menu()
        return True
    if command == "help" or command == 7:
        show_contacts_submenu()
        return True
    if command in exit_commands or command == 8:
        pretty_title("Goodbye!")
        addressbook.save_data()
        sys.exit(0)
        # return False
    else:
        print(f"{bcolors.WARNING}Unknown command{bcolors.ENDC}")


def notes_handler(command):
    if not isinstance(command, int):
        try:
            os.system('clear') | os.system('cls')
            command = get_close_matches(command, all_commands, n=1, cutoff=0.5)[0]
            print(f'{bcolors.OKGREEN}You have chosen a command: {bcolors.HEADER}{command}{bcolors.ENDC}')
        except IndexError:
            print(f"{bcolors.WARNING}Sorry, I don't understand. Please try again.{bcolors.ENDC}")
            return True
    if command == "add" or command == 0:
        try:
            os.system('clear') | os.system('cls')
            pretty_title(f"Add a note please:\n{'=' * 40}")
            title = input("Enter title: ").title().strip()
            text = input("Enter text: ").strip()
            teg = input("Enter tag like teg1, teg2: ").strip()
            show_print(f'{title}; {text}; {teg}')
            note = NoteBookRecord(Name(title), NoteBookText(text))
            tegs_list = teg.split(',')
            for tg in tegs_list:
                if tg != '':
                    note.add_teg(NoteBookTeg(tg.strip()))
            notebook.add_record(note)
            print(f"{bcolors.OKGREEN}Note was added successfully!{bcolors.ENDC}")
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
                    print(f"{bcolors.OKGREEN}Record: {bcolors.HEADER}{old_title}{bcolors.OKGREEN} was updated to: {bcolors.HEADER}{new_value}{bcolors.ENDC}")
                    return True
            print(f"{bcolors.WARNING}Note title {bcolors.HEADER}{old_title}{bcolors.OKGREEN} was not found!{bcolors.ENDC}")
            notebook.save_data()
            return True
        if updated_position == 1:
            name = input("Enter name: ").title().strip()
            new_text = input("Enter new text: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.text = NoteBookText(new_text)
            print(f'{bcolors.WARNING}Note title :{bcolors.HEADER}{name}{bcolors.WARNING} is not found!{bcolors.ENDC}')
            notebook.save_data()
            return True
        if updated_position == 2:
            name = input("Enter name: ").title().strip()
            new_teg = input("Enter new tag: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.add_teg(NoteBookTeg(new_teg))
            print(f'{bcolors.WARNING}Note title {bcolors.HEADER}{name}{bcolors.WARNING} was not found!{bcolors.ENDC}')
            notebook.save_data()
            return True
        if updated_position == 3:
            name = input("Enter name: ").title().strip()
            new_teg = input("Enter del tag: ").strip()
            note = notebook.get(name, -1)
            if note != -1:
                note.del_teg(new_teg)
            print(f'{bcolors.WARNING}Note title {bcolors.HEADER}{name}{bcolors.WARNING} was not found!{bcolors.ENDC}')
            notebook.save_data()
            return True
        if updated_position == 4:
            show_notes_submenu()
            return True
    if command in back_to_menu_commands or command == 6:
        show_menu()
        return True
    if command == "help" or command == 7:
        show_notes_submenu()
        return True
    if command in exit_commands or command == 8:
        pretty_title("Goodbye!")
        notebook.save_data()
        sys.exit(0)
        # return False
    else:
        print(f"{bcolors.WARNING}Unknown command{bcolors.ENDC}")
