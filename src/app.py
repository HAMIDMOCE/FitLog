from src.menu import Menu
from src.database import DatabaseManager
from src.statistics import Statistics
from src.weight import Weight
from src.reports import Reports

from rich.console import Console

class App:

    def __init__(self):
        self.menu = Menu()
        self.database = DatabaseManager()

        self.console = Console()

        self.weight = Weight(self.database, self.console)
        self.statistics = Statistics(self.database, self.console)
        self.reports = Reports(self.database, self.console)

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
            return self.weight.add_daily_weight()
        
        elif choice == 2:
            return self.weight.view_weight_history()

        elif choice == 3:
            return self.statistics.show()

        elif choice == 4:
            return self.reports.show_weight_change_report()

        elif choice == 5:
            return False, "\nGoodbye!"

        else:
            return True, "\nInvalid choice."