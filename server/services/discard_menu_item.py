from commons.literals import DB_CONFIG
from datetime import datetime
from database.db_connection import DatabaseConnection

class DiscardMenu:
    def check_last_discard_list_generation_date(self):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = """select max(discard_list_generation_date) from discarded_items;"""
            last_list_deneration_date = db.fetch_all(query)
            last_list_deneration_date = datetime.strptime(last_list_deneration_date[0][0], "%Y-%m-%d")
            current_date = datetime.now()
            difference_in_days = (current_date.date() - last_list_deneration_date.date()).days
            return difference_in_days
        except Exception as e:
            if("'lnc.discarded_items' doesn't exist" in str(e)):
                return 30
            else:
                print(e)

    def add_items_to_discard_list(self):
        try:
            if(self.check_last_discard_list_generation_date() >= 30):
                db = DatabaseConnection(DB_CONFIG)
                db.connect()
                query = """create or replace view discarded_items as 
                select f.item_id, item_name, avg(rating) as average_rating, avg(sentiment_score) as average_sentiment, CAST(CURDATE() AS CHAR) AS discard_list_generation_date 
                from feedback f join menu_item m on f.item_id = m.item_id
                where m.is_deleted = 0 group by f.item_id having average_rating < 27 and average_sentiment < 0;"""
                db.execute_query(query)
                db.disconnect()
                status = "Items Added to discarded list"
            else:
                status = "You have already generated discard item list in this month."
        except Exception as e:
            print(e)
            status = "Error in adding items to discarded list"
        response = {"action": "GENERATE_DISCARD_MENU_ITEM","status": status}
        return response
    
    def review_discarded_item_list(self):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = """select * from discarded_items;"""
            discarded_items = db.fetch_all(query)
            status = "Fetched list for discarded items"
            db.disconnect()
        except Exception as e:
            status = "Error in fetching discarded items :( please try later."
            discarded_items = None
        response = {"action": "REVIEW_DISCARDED_ITEM_LIST", "discarded_items": discarded_items, "status": status}
        return response
    