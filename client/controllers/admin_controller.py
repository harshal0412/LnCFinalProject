from server.services.menu_item import MenuItem
import json

class AdminController:
    def add_menu_item(self):
        action = "ADD_MENU_ITEM"
        item_name = input("\nEnter item name: ")
        price = int(input("\nEnter item price: "))
        availability_status = int(input("\nEnter availability status (1 for available 0 for not available): "))
        item_category = int(input("\nEnter item category (1 -> Breakfast, 2 -> Lunch, 3 -> Dinner): "))
        item = MenuItem(item_name=item_name,price=price,availability_status=availability_status,item_category=item_category)
        item_detail_in_json = item.to_dict()
        spice_level = input("Enter spice level (High, Medium, Low): ")
        dietry = input("Enter dietry (Veg, Non-veg): ")
        item_property = {"spice_level": spice_level, "dietry": dietry}
        item_detail_to_send_to_server = json.dumps({'action': action, 'data': item_detail_in_json,"item_property": item_property})
        return item_detail_to_send_to_server
    
    def update_item_availability(self):
        action = "UPDATE_AVAILABILITY"
        item_id = int(input("\nEnter item_id to update: "))
        availability_status = int(input("\nEnter availability status (1 for available 0 for not available): "))
        item = MenuItem(item_id=item_id,availability_status=availability_status)
        item_detail_in_json = item.to_dict()
        item_detail_to_send_to_server = json.dumps({'action': action, 'data': item_detail_in_json})
        return item_detail_to_send_to_server
    
    def delete_item_from_menu(self):
        action = "DELETE_ITEM"
        item_id = int(input("\nEnter item_id to delete: "))
        item = MenuItem(item_id=item_id)
        item_detail_in_json = item.to_dict()
        item_detail_to_send_to_server = json.dumps({'action': action, 'data': item_detail_in_json})
        return item_detail_to_send_to_server
        
    def fetch_complete_menu(self):
        action = "FETCH_COMPLETE_MENU"
        item_detail_to_send_to_server = json.dumps({'action': action})
        return item_detail_to_send_to_server
    
    def view_complete_feedback(self):
        action = "VIEW_FEEDBACK"
        item_detail_to_send_to_server = json.dumps({'action': action})
        return item_detail_to_send_to_server
    
    def update_item_property(self):
        action = "UPDATE_ITEM_PROPERTY"
        item_id = int(input("\nEnter item_id: "))
        spice_level = input("Enter spice level (High, Medium, Low): ")
        dietry = input("Enter dietry (Veg, Non-veg): ")
        item_property = {"item_id": item_id,"spice_level": spice_level, "dietry": dietry}
        item_detail_to_send_to_server = json.dumps({'action': action, "data":item_property})
        return item_detail_to_send_to_server