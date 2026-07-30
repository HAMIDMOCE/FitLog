class ReportMenu:

    def display(self):
        print("=" * 40)
        print("Reports".center(40))
        print("=" * 40)
        print()
        print("1. Weight Change Report")
        print("2. Weekly Report")
        print("3. Monthly Report")
        print("4. Back")
        print()
        print("=" * 40)

    def get_choice(self):
        while True:
            choice = input("\nEnter your choice: ").strip()

            if not choice:
                print("Choice cannot be empty.")
                continue

            try:
                choice = int(choice)

                if 1 <= choice <= 4:
                    return choice

                print("Please enter a number between 1 and 4.")

            except ValueError:
                print("Please enter a valid number.")