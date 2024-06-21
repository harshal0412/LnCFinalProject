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

    def display_menu(self):
        return self.db.display_menu()

    def get_menu_recommendations(self):
        return self.db.get_menu_recommendations()

    def roll_out_menu(self, n_breakfast, n_lunch, n_dinner):
        return self.db.roll_out_menu(n_breakfast, n_lunch, n_dinner)

    def generate_monthly_report(self):
        return self.db.generate_monthly_report()

    def tomorrows_menu(self):
        return self.db.tomorrows_menu()

    def give_feedback(self, feedback):
        return self.db.give_feedback(feedback)
