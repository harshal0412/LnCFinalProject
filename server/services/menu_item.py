from database.db_connection import DatabaseConnection
from commons.literals import *

class MenuItem:
    def __init__(self, item_id=None, item_name=None, price=None, availability_status=None, item_category=None):
        self.item_id = item_id
        self.item_name = item_name
        self.price = price
        self.availability_status = availability_status
        self.item_category = item_category

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "price": self.price,
            "availability_status": self.availability_status,
            "item_category": self.item_category,
        }
    
    @classmethod
    def fetch_complete_menu(cls):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = "SELECT * FROM menu_item where is_deleted = 0;"
            menu_items = db.fetch_all(query)
            db.disconnect()
        except Exception as e:
            print("Error in fetching complete Menu")
        response = {"action": "FETCH_COMPLETE_MENU", "data":menu_items}
        return response
    
    def get_item_detail_by_id(self,item_id):
        db = DatabaseConnection(DB_CONFIG)
        db.connect()
        query = f"SELECT * FROM menu_item where item_id in ({item_id});"
        menu_items = db.fetch_all(query)
        db.disconnect()
        return menu_items
    
    def view_next_day_menu(self, data):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = f"""select pref.item_id, pref.item_name from (SELECT infd.item_id, infd.item_name,
                CASE WHEN ep.dietry = f.dietry THEN 1 ELSE 0 END AS dietary_match,
                CASE WHEN ep.spice_level = f.spice_level THEN 1 ELSE 0 END AS spice_level_match
            FROM user_profile ep
            LEFT JOIN item_for_next_day infd ON 1=1
            LEFT JOIN meal_property f ON infd.item_id = f.item_id
            WHERE ep.user_id = {data['user_id']}
            ORDER BY dietary_match DESC,
                    spice_level_match DESC) pref;
            """
            next_day_menu = db.fetch_all(query)
            if(len(next_day_menu) == 0):
                query = """select item_id, item_name from item_for_next_day;"""
                next_day_menu = db.fetch_all(query)
            db.disconnect()
        except Exception as e:
            print("Error in next day menu items")
        response = {"action": "VIEW_NEXT_DAY_MENU", "data":{"next_day_menu": next_day_menu}}
        return response