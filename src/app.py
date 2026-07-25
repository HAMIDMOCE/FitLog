from src.menu import Menu

class App:

    def __init__(self):
        self.menu = Menu()

    def run(self):
        self.menu.display()

        choice = self.menu.get_choice()
        print(f"You selected: {choice}")