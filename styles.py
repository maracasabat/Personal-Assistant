from prettytable import PrettyTable

records = PrettyTable()

records.field_names = ["Name", "Phone", "Email", "Address", "Birthday"]

names = ["Vitya", "Vasya", "Petya"]
phones = ["+380937777777", "+380937777777", "+380937777777"]
emails = ["sash@icloud.com", "goh@icloud.com", "loh@icloud.com"]
addresses = ["Kiev", "Lviv", "Odessa"]
birthdays = ["01.01.2000", "01.01.2000", "01.01.2000"]

for name, phone, email, address, birthday in zip(names, phones, emails, addresses, birthdays):
    records.add_row([name, phone, email, address, birthday])


def show_records(notes):
    return print(records)
