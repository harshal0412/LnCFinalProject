import pyodbc

class DBOperations:
    def __init__(self):
        self.connection = None

    def connect(self, db_config):
        try:
            conn_str = ';'.join([f"{key}={value}" for key, value in db_config.items()])
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
            cursor.execute("SELECT role FROM Users WHERE name = ? AND password = ?", username, password)
            result = cursor.fetchone()
            if result:
                return True, result.role
            else:
                return False, None
        else:
            return False, None

    def add_menu_item(self, name, price, availability):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Menu (name, price, availability) VALUES (?, ?, ?)", name, price, availability)
            self.connection.commit()
            return "Menu item added successfully"
        else:
            return "Database connection not established"

    def update_menu_item(self, item_id, price, availability):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE Menu SET price = ?, availability = ? WHERE ID = ?", price, availability, item_id)
            self.connection.commit()
            return "Menu item updated successfully"
        else:
            return "Database connection not established"

    def delete_menu_item(self, item_id):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Menu WHERE ID = ?", item_id)
            self.connection.commit()
            return "Menu item deleted successfully"
        else:
            return "Database connection not established"
