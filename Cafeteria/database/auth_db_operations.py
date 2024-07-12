class AuthDBOperations:
    def __init__(self, connection):
        self.connection = connection

    def signup(self, username, password, role):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Users (name, password, role) VALUES (?, ?, ?)", username, password, role)
            self.connection.commit()
            return "Signup successful"
        else:
            return "Database connection not established"

    def login(self, username, password):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT role, Emp_id FROM Users WHERE name = ? AND password = ?", username, password)
            result = cursor.fetchone()
            if result:
                return True, result.role, result.Emp_id
            else:
                return False, None
        else:
            return False, None
