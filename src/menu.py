class Menu:

    def display(self):
        print("=" * 40)
        print("FitLog".center(40))
        print("=" * 40)
        print()
        print("1. Add Daily Weight")
        print("2. View Weight History")
        print("3. Statistics")
        print("4. Reports")
        print("5. Exit")
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
                return choice

            except ValueError:
                print("Invalid input.")