from view import show_menu, command_handler
from styles import records, show_records, pretty_title, bcolors


def main():
    pretty_title("Hi! Welcome to Personal Assistant Bot")
    # print(f"{bcolors.OKBLUE}Hi!{bcolors.HEADER} Welcome to Personal Assistant Bot{bcolors.ENDC}")
    show_menu()
    command = input("Write your command: ").casefold().strip()

    while command_handler(command):
        command = input("Write your command: ").casefold().strip()


if __name__ == "__main__":
    main()
