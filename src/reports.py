from rich.table import Table

class Reports:

    def __init__(self, database, console):
        self.database = database
        self.console = console

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

    def print_header(self, title):
        print("=" * 40)
        print(title.center(40))
        print("=" * 40)
        print()