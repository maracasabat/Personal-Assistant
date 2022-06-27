from prettytable import PrettyTable

records = PrettyTable()
notes = PrettyTable()
test_notes = PrettyTable()


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


def show_notes(notebook):
    notes.field_names = ["Title", "Text", "Tags"]
    notes.clear_rows()
    notes_list = []
    for k, v in notebook.items():
        value = str(v).split(',')
        new_note = [k] + value
        notes_list.append(new_note)

    for note in notes_list:
        notes.add_row(note)

    return print(notes)


def show_print(note):
    test_notes.field_names = ["Title", "Text", "Tags"]
    test_notes.add_row(note)

    return print(test_notes)
