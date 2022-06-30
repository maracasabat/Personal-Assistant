from prettytable import PrettyTable
from termcolor2 import colored

records = PrettyTable()
notes = PrettyTable()
test_notes = PrettyTable()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def pretty_title(text):
    return print(colored(text, color='blue'))


#  ============= табличка для записей  =============

def show_records(addressbook):
    records.field_names = ["Name", "Phone", "Email", "Address", "Birthday"]
    records.clear_rows()
    records_list = []
    for k, v in addressbook.items():
        value = str(v).split(',')
        new_record = [k] + value
        records_list.append(new_record)

    for record in records_list:
        records.add_row(record)

    return print(records)


#  ============= табличка для всех заметок  =============

def show_notes(notebook):
    notes.field_names = ["Title", "Tags", "Text"]
    notes.clear_rows()
    for note in notebook.values():
        record = str(note).split(';')
        notes.add_row(record)

    return print(notes)


# ============= табличка для созданной заметки  =============
def show_print(note):
    pretty_title(f'Your Note:')
    test_notes.field_names = ["Title", "Text", "Tags"]
    note = str(note).split(';')
    test_notes.clear_rows()
    test_notes.add_row(note)

    return print(test_notes)
