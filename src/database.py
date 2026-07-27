from mysql import connector

class DatabaseManager:

    def __init__(
            self,
            host="localhost",
            port=3306,
            user="root",
            password="Hamid.mo83",
            database_name="FitLog" 
            ):

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database_name = database_name

        self.connection = None
        self.cursor = None

    def connect_server(self):
        try:
            self.connection = connector.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password
            )

            self.cursor = self.connection.cursor()
            return True, "Connected to MySQL server successfully."

        except connector.Error as error:
            return False, str(error)

    def create_database(self):
        try:
            self.cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {self.database_name}"
            )

            self.connection.commit()

            return True, "Database created successfully."

        except connector.Error as error:
            return False, str(error)

    def connect_database(self):
        status, message = self.close()

        if not status:
            return False, message

        try:
            self.connection = connector.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.database_name
            )

            self.cursor = self.connection.cursor()
            return True, f"Connected to '{self.database_name}' successfully."

        except connector.Error as error:
            return False, str(error)

    def create_table(self):
        try:
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS weights(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    weight DECIMAL(5, 2) NOT NULL,
                    recorded_at DATETIME NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            self.connection.commit()

            return True, "Tables created successfully."

        except connector.Error as error:
            return False, str(error)

    def close(self):
        try:
            if self.cursor is not None:
                self.cursor.close()
                self.cursor = None

            if self.connection is not None:
                if self.connection.is_connected():
                    self.connection.close()

                self.connection = None

        except connector.Error as error:
            return False, str(error)

        return True, "Connection closed successfully."

    def initialize(self):
        steps = [
            self.connect_server,
            self.create_database,
            self.connect_database,
            self.create_table,
        ]

        messages = []

        for step in steps:
            status, message = step()
            messages.append(message)

            if not status:
                return False, messages

        return True, messages