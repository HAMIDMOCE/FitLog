from src.menu import Menu
from src.database import DatabaseManager

from datetime import datetime

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
            return self.add_daily_weight()
        
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

    def print_header(self, title):
        print("=" * 40)
        print(title.center(40))
        print("=" * 40)
        print()

    def add_daily_weight(self):
        self.print_header("ADD DAILY WEIGHT")

        while True:
            weight = input("Enter weight: ").strip()
        
            if not weight:
                print("Weight cannot be empty.")
                continue
        
            try:
                weight = float(weight)
                if weight < 20 or weight > 400:
                    print("Weight should be between 20 and 400.\n")
                    continue

                break
        
            except ValueError:
                print("Invalid input.")


        while True:
            date_input = input("Enter date (YYYY-MM-DD): ")
        
            try:
                recorded_at = datetime.strptime(date_input, "%Y-%m-%d")
                break
        
            except ValueError:
                print("Invalid date.")

        if self.database.weight_exists(recorded_at):
            print("Weight already recorded for this date.")
                        
            while True:
                choose = input("Do you want update this weight? (y/n) ").strip().lower()
        
                if choose in ("y", "n"):
                     break
        
                print("Please enter y or n.\n")
        
            if choose == "y":
                return self.database.update_weight(weight, recorded_at)

            return True, "Operation cancelled."

        return self.database.insert_weight(weight, recorded_at)