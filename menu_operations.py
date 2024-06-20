# menu_operations.py

class MenuOperations:
    def __init__(self, db):
        self.db = db

    def add_menu_item(self, name, price, availability):
        return self.db.add_menu_item(name, price, availability)

    def update_menu_item(self, item_id, price, availability):
        return self.db.update_menu_item(item_id, price, availability)

    def delete_menu_item(self, item_id):
        return self.db.delete_menu_item(item_id)
