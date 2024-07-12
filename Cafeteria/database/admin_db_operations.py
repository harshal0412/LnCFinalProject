class AdminDBOperations:
    def __init__(self, connection):
        self.connection = connection

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

    def display_menu(self):
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Menu")
            result = cursor.fetchall()
            menu_items = [f"ID: {row.ID}, Name: {row.name}, Price: {row.price}, Availability: {row.availability}" for row in result]
            return "\n".join(menu_items)
        else:
            return "Database connection not established"
