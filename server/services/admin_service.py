from commons.literals import DB_CONFIG
from database.db_connection import DatabaseConnection
from services.notification_service import Notification

class AdminService:

    def fetch_latest_item_id(self):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = "select max(item_id) as latest_id from menu_item;"
            latest_id = db.fetch_all(query)[0][0]
            db.disconnect()
        except:
            print("No item added recently")
        return latest_id
    
    def add_menu_item(self,data,item_property):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = '''
            insert into menu_item (item_name, price, availability_status, item_category, is_deleted) values (%s,%s,%s,%s,0);
            '''
            values = (data['item_name'], data['price'], data['availability_status'], data['item_category'])
            db.execute_query(query, values)
            db.disconnect()
            latest_id = self.fetch_latest_item_id()
            item_property['item_id'] = latest_id
            response = self.update_item_properties(item_property)
            message = f"New item {data['item_name']} has been added to menu."
            sender = "ADMIN"
            notification = Notification(message,sender)
            notification.send_notification()
            status = "Item added successfully"
        except Exception as e:
            status = "Item not added"
        response = {"action": "ADD_MENU_ITEM", "status": status}
        return response
    
    def update_item_properties(self, item_property):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = """insert into meal_property values (%s,%s,%s);"""
            values = (item_property['item_id'], item_property['spice_level'], item_property['dietry'])
            db.execute_query(query, values)
            db.disconnect()
            status = "Item properties updated successfully"
        except Exception as e:
            status = "Error while updating item properties"
        response = {"action": "UPDATE_ITEM_PROPERTY", "status": status}
        return response

    def update_item_availability(self,data):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = '''
            update menu_item set availability_status = %s where item_id = %s;
            '''
            values = (data['availability_status'], data['item_id'])
            db.execute_query(query, values)
            db.disconnect()
            status = "Availability updated successfully"
        except Exception as e:
            print(e)
            status = "Error in updating availability"
        response = {"action": "UPDATE_AVAILABILITY", "status": status}
        return response
    
    def delete_item_from_menu(self,data):
        try:
            db = DatabaseConnection(DB_CONFIG)
            db.connect()
            query = '''
            update menu_item set is_deleted = 1 where item_id = %s;
            '''
            values = (data['item_id'],)
            db.execute_query(query, values)
            db.disconnect()
            status = "Item deleted successfully"
        except Exception as e:
            status = "Error in deleting item"
        response = {"action": "DELETE_ITEM", "status": status}
        return response
