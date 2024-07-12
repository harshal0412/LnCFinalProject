import pyodbc

class DBConnection:
    def __init__(self, db_config):
        self.connection = None
        self.db_config = db_config

    def connect(self):
        try:
            conn_str = ';'.join([f"{key}={value}" for key, value in self.db_config.items()])
            self.connection = pyodbc.connect(conn_str)
            print("Database connection successful")
        except pyodbc.Error as e:
            print("Failed to connect to the database")
            print(e)
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")
