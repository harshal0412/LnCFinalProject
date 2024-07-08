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

    def roll_out_menu(self, breakfast_ids, lunch_ids, dinner_ids):
        return self.db.roll_out_menu(breakfast_ids, lunch_ids, dinner_ids)

    def generate_monthly_report(self):
        return self.db.generate_monthly_report()

    def tomorrows_menu(self):
        return self.db.tomorrows_menu()
   
    def employee_voting(self,item_id):
        return self.db.employee_voting(item_id)

    def give_feedback(self, menu_id, feedback, rating):
        return self.db.give_feedback(menu_id, feedback, rating)

    def get_item_detail_by_id(self, ids):
        return self.db.get_item_detail_by_id(ids)
