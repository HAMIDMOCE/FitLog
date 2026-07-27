from src.menu import Menu
from src.database import DatabaseManager

class App:

    def __init__(self):
        self.menu = Menu()
        self.database = DatabaseManager()

    def run(self):
        status, messages = self.database.initialize()

        for message in messages:
            print(message)

        print()

        if not status:
            return
        
        while True:
            self.menu.display()

            choice = self.menu.get_choice()

            continue_running, message = self.handle_choice(choice)

            print(message)

            if not continue_running:
                break

    def handle_choice(self, choice):
        if choice == 1:
            return True, "\nAdd Daily Weight selected."

        elif choice == 2:
            return True, "\nView Weight History selected."

        elif choice == 3:
            return True, "\nStatistics selected."

        elif choice == 4:
            return True, "\nReports selected."

        elif choice == 5:
            return False, "\nGoodbye!"

        else:
            return True, "\nInvalid choice."