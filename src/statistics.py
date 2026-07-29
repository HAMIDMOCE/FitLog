from rich.console import Console
from rich.table import Table

class Statistics:

    def __init__(self, database):
        self.database = database
        self.console = Console()

    def show(self):
        status, total_records = self.database.get_total_records()
        if not status:
            return False, total_records

        status, current_weight = self.database.get_current_weight()
        if not status:
            return False, current_weight

        status, highest_weight = self.database.get_highest_weight()
        if not status:
            return False, highest_weight

        status, lowest_weight = self.database.get_lowest_weight()
        if not status:
            return False, lowest_weight

        status, average_weight = self.database.get_average_weight()
        if not status:
            return False, average_weight

        table = Table(
            title="STATISTICS",
            show_lines=True
        )
        table.add_column("Metric".center())
        table.add_column("Value".center())

        table.add_row(
            "Total Records",
            f"{total_records}" if total_records is not None else "-"
        )
        table.add_row(
            "Current Weight",
            f"{current_weight:.2f}" if current_weight is not None else "-"
        )
        table.add_row(
            "Highest Weight",
            f"{highest_weight:.2f}" if highest_weight is not None else "-"
        )
        table.add_row(
            "Lowest Weight",
            f"{lowest_weight:.2f}" if lowest_weight is not None else "-"
        )
        table.add_row(
            "Average Weight",
            f"{average_weight:.2f}" if average_weight is not None else "-"
        )

        self.console.print(table)

        return True, ""