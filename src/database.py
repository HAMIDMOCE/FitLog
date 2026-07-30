from mysql import connector
from datetime import datetime, timedelta

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
                    recorded_at DATETIME NOT NULL UNIQUE,
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

    def weight_exists(self, recorded_at):
        try:
            self.cursor.execute(
                """
                SELECT id FROM weights
                WHERE recorded_at = %s
                """,
                (recorded_at,)
            )

            record = self.cursor.fetchone()

            return record is not None

        except connector.Error:
            return False

    def insert_weight(self, weight, recorded_at):
        try:
            self.cursor.execute(
                """
                INSERT INTO weights (weight, recorded_at)
                VALUES (%s, %s)
                """,
                (weight, recorded_at)
            )

            self.connection.commit()

            return True, "Weight added successfully."

        except connector.Error as error:
            return False, str(error)

    def update_weight(self, weight, recorded_at):
        try:
            self.cursor.execute(
                """
                UPDATE weights SET weight=%s
                WHERE recorded_at = %s
                """,
                (weight, recorded_at)
            )

            self.connection.commit()

            count = self.cursor.rowcount

            if count == 0:
                return False, "No weight record found for this date."

            return True, "Updated successfully."

        except connector.Error as error:
            return False, str(error)

    def get_all_weights(self):
        try:
            self.cursor.execute(
                """
                SELECT id, weight, recorded_at, added_at
                FROM weights
                ORDER BY recorded_at ASC
                """
            )

            return True, self.cursor.fetchall()

        except connector.Error as error:
            return False, str(error)

    def get_total_records(self):
        try:
            self.cursor.execute(
                """
                SELECT COUNT(*)
                FROM weights
                """
            )

            return True, self.cursor.fetchone()[0]

        except connector.Error as error:
            return False, str(error)

    def get_current_weight(self):
        try:
            self.cursor.execute(
                """
                SELECT weight
                FROM weights
                ORDER BY recorded_at DESC
                LIMIT 1
                """
            )
            
            result = self.cursor.fetchone()

            if result is None:
                return True, None

            return True, result[0]

        except connector.Error as error:
            return False, str(error)

    def get_highest_weight(self):
        try:
            self.cursor.execute(
                """
                SELECT MAX(weight)
                FROM weights
                """
            )

            result = self.cursor.fetchone()
            
            return True, result[0]

        except connector.Error as error:
            return False, str(error)

    def get_lowest_weight(self):
        try:
            self.cursor.execute(
                """
                SELECT MIN(weight)
                FROM weights
                """
            )

            result = self.cursor.fetchone()
            
            return True, result[0]

        except connector.Error as error:
            return False, str(error)

    def get_average_weight(self):
        try:
            self.cursor.execute(
                """
                SELECT AVG(weight)
                FROM weights
                """
            )

            result = self.cursor.fetchone()
            
            return True, result[0]

        except connector.Error as error:
            return False, str(error)

    def get_first_and_last_weight(self):
        try:
            self.cursor.execute(
                """
                SELECT weight
                FROM weights
                ORDER BY recorded_at DESC
                LIMIT 1
                """
            )

            last_weight = self.cursor.fetchone()

            self.cursor.execute(
                """
                SELECT weight
                FROM weights
                ORDER BY recorded_at ASC
                LIMIT 1
                """
            )

            first_weight = self.cursor.fetchone()

            if first_weight is None or last_weight is None:
                return True, None, None

            return True, first_weight[0], last_weight[0]

        except connector.Error as error:
            return False, str(error)

    def get_weekly_records(self):
        today = datetime.today()
        week_day = today.weekday()

        start_of_week = today - timedelta(days=week_day)
        start_of_week= start_of_week.replace(
            hour=0,
            minute=0,
            second=0
        )

        end_of_week = start_of_week + timedelta(days=6)
        end_of_week = end_of_week.replace(
            hour=23,
            minute=59,
            second=59
        )

        try:
            self.cursor.execute(
                """
                SELECT weight, recorded_at
                FROM weights
                WHERE recorded_at BETWEEN %s AND %s
                ORDER BY recorded_at ASC
                """,
                (start_of_week, end_of_week)
            )

            records = self.cursor.fetchall()

            return True, records

        except connector.Error as error:
            return False, str(error)

    def get_monthly_records(self):
        today = datetime.today()
        
        start_of_month = today.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

        if start_of_month.month == 12:
            next_month = start_of_month.replace(
                year=start_of_month.year + 1,
                month=1
            )
        else:
            next_month = start_of_month.replace(
                month=start_of_month.month + 1
            )

        end_of_month = next_month - timedelta(seconds=1)

        try:
            self.cursor.execute(
                """
                SELECT weight, recorded_at
                FROM weights
                WHERE recorded_at BETWEEN %s AND %s
                ORDER BY recorded_at ASC
                """,
                (start_of_month, end_of_month)
            )

            records = self.cursor.fetchall()

            return True, records

        except connector.Error as error:
            return False, str(error)        