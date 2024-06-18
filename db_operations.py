import pyodbc

class Database:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(**self.config)
            print("Connected to SQL Server database")
        except pyodbc.Error as e:
            print(f"Error: {e}")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            print("SQL Server connection is closed")

    def signup(self, username, password, role):
        if not self.connection:
            return "No database connection"
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO Users (name, password, role) VALUES (?, ?, ?)", (username, password, role))
            self.connection.commit()
            return "Signup successful"
        except pyodbc.Error as err:
            return f"Signup failed: {err}"
        finally:
            cursor.close()

    def login(self, username, password):
        if not self.connection:
            return "No database connection"
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE name = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return "Login successful"
        else:
            return "Login failed"
