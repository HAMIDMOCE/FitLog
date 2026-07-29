from datetime import datetime

from rich.table import Table

class Weight:

    def __init__(self, database, console):
        self.database = database
        self.console = console

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
                choice = input("Do you want update this weight? (y/n) ").strip().lower()
                
                if choice in ("y", "n"):
                     break
                
                print("Please enter y or n.\n")

            if choice == "y":
                return self.database.update_weight(weight, recorded_at)
            
            return True, "Operation cancelled."

        return self.database.insert_weight(weight, recorded_at)

    def view_weight_history(self):
        self.print_header("WEIGHT HISTORY")
    
        status, records = self.database.get_all_weights()
    
        if not status:
            return False, records
    
        if not records:
            return True, "No records found."
    
        table = Table(
            title="Weight History",
            show_lines=True
        )
        table.add_column("ID")
        table.add_column("Weight")
        table.add_column("Recorded Date")
        table.add_column("Added At")
    
        for record in records:
            id_, weight, recorded_at, added_at = record
    
            table.add_row(str(id_), str(weight), str(recorded_at), str(added_at))
    
        self.console.print(table)
    
        return True, ""

    def print_header(self, title):
        print("=" * 40)
        print(title.center(40))
        print("=" * 40)
        print()