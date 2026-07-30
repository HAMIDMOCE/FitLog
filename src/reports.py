from src.report_menu import ReportMenu

from rich.table import Table

class Reports:

    def __init__(self, database, console):
        self.database = database
        self.console = console

        self.menu = ReportMenu()

    def show(self):
        while True:
            self.menu.display()

            choice = self.menu.get_choice()

            if choice == 1:
                status, message = self.show_weight_change_report()

            elif choice == 2:
                status, message = self.show_weekly_report()

            elif choice == 3:
                status, message = self.show_monthly_report()

            elif choice == 4:
                return True, ""

            if not status:
                return False, message

            if message:
                print(message)

    def show_weight_change_report(self):
        self.print_header("Weight Change Report")

        status, first_weight, last_weight = self.database.get_first_and_last_weight()

        if not status:
            return False, first_weight

        if first_weight is None or last_weight is None:
            return True, "No records found."

        difference = last_weight - first_weight

        if difference > 0:
            change_status = "Weight Gained"

        elif difference < 0:
            change_status = "Weight Lost"

        else:
            change_status = "No Change"

        table = Table(
            title="Weight Change Report",
            show_lines=True
        )

        table.add_column("Metric", justify="center")
        table.add_column("Value", justify="center")

        table.add_row("First Weight", f"{first_weight:.2f}")
        table.add_row("Last Weight", f"{last_weight:.2f}")
        table.add_row(
            "Difference",
            f"+{difference:.2f}" if difference >= 0 else f"{difference:.2f}"
        )
        table.add_row("Status", change_status)

        self.console.print(table)

        return True, ""

    def show_weekly_report(self):
        self.print_header("Weekly Report")

        status, records = self.database.get_weekly_records()

        if not status:
            return False, records

        if not records:
            return True, "No records found for this week."

        weights = [record[0] for record in records]

        first_weight = weights[0]
        last_weight = weights[-1]
        highest_weight = max(weights)
        lowest_weight = min(weights)
        average_weight = sum(weights) / len(weights)
        difference = last_weight - first_weight

        if difference > 0:
            change_status = "Weight Gained"
        
        elif difference < 0:
            change_status = "Weight Lost"
        
        else:
            change_status = "No Change"

        table = Table(
            title="Weekly Report",
            show_lines=True
        )

        table.add_column("Metric", justify="center")
        table.add_column("Value", justify="center")

        table.add_row("First Weight", f"{first_weight:.2f}")
        table.add_row("Last Weight", f"{last_weight:.2f}")
        table.add_row("Highest Weight", f"{highest_weight:.2f}")
        table.add_row("Lowest Weight", f"{lowest_weight:.2f}")
        table.add_row("Average Weight", f"{average_weight:.2f}")
        table.add_row(
            "Difference",
            f"+{difference:.2f}" if difference >= 0 else f"{difference:.2f}"
        )
        table.add_row("Status", change_status)

        self.console.print(table)

        return True, ""

    def show_monthly_report(self):
        self.print_header("Monthly Report")

        status, records = self.database.get_monthly_records()

        if not status:
            return False, records
        
        if not records:
            return True, "No records found for this month."

        weights = [record[0] for record in records]

        first_weight = weights[0]
        last_weight = weights[-1]
        highest_weight = max(weights)
        lowest_weight = min(weights)
        average_weight = sum(weights) / len(weights)
        difference = last_weight - first_weight

        if difference > 0:
            change_status = "Weight Gained"
        
        elif difference < 0:
            change_status = "Weight Lost"
        
        else:
            change_status = "No Change"

        table = Table(
            title="Monthly Report",
            show_lines=True
        )

        table.add_column("Metric", justify="center")
        table.add_column("Value", justify="center")

        table.add_row("First Weight", f"{first_weight:.2f}")
        table.add_row("Last Weight", f"{last_weight:.2f}")
        table.add_row("Highest Weight", f"{highest_weight:.2f}")
        table.add_row("Lowest Weight", f"{lowest_weight:.2f}")
        table.add_row("Average Weight", f"{average_weight:.2f}")
        table.add_row(
            "Difference",
            f"+{difference:.2f}" if difference >= 0 else f"{difference:.2f}"
        )
        table.add_row("Status", change_status)

        self.console.print(table)

        return True, ""        

    def print_header(self, title):
        print("=" * 40)
        print(title.center(40))
        print("=" * 40)
        print()