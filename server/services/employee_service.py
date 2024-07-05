from commons.literals import DB_CONFIG
from database.db_connection import DatabaseConnection
import datetime
from services.sentiment_analyzer import SentimentAnalyzer


class EmployeeService:
    
    def vote_for_food_item(self, data):
        try:
            selection_date = str(datetime.datetime.today().date())
            for item_id in data['items_to_vote']:
                print(item_id)
                db = DatabaseConnection(DB_CONFIG)
                db.connect()
                query = '''insert into voted_item (user_id,item_id,selection_date) values (%s,%s,%s)'''
                values = (data['user_id'], item_id, selection_date)
                db.execute_query(query, values)
                db.disconnect()
            status = "Food item voted successfully"
        except Exception as e:
            status = "Error in next day menu items"
        response = {"action": "VOTE_FOR_FOOD_ITEM", "status": status}
        return response
    
    def view_discarded_items(self):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = """select d.item_id, d.item_name from discarded_items d join menu_item m on m.item_id = d.item_id
            where m.is_deleted = 0;"""
            discarded_items = db.fetch_all(query)
            status = "Fetched discarded items"
            db.disconnect()
        except Exception as e:
            status = "Error in fetching discarded items"
        response = {"action": "VIEW_DISCARDED_ITEMS", "discarded_items": discarded_items, "status": status}
        return response
    
    def update_profile(self, data):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = "insert into user_profile values (%s,%s,%s);"
            values = (data['user_id'],data['spice_level'],data['dietry'])
            db.execute_query(query, values)
            db.disconnect()
            status = "User profile updated successfully"
        except Exception as e:
            status = "Error while updating user profile try again later"
        response = {"action": "UPDATE_PROFILE", "status": status} 
        return response