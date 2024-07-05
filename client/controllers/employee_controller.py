import json

class EmployeeController:
    
    def fetch_complete_menu(self):
        action = "FETCH_COMPLETE_MENU"
        item_detail_to_send_to_server = json.dumps({'action': action})
        return item_detail_to_send_to_server
    
    def provide_feedback(self,user_id):
        action = "PROVIDE_FEEDBACK"
        item_id = int(input("Enter the item_id: "))
        comment = input("Enter comment: ")
        rating = float(input("Enter rating out of 5: "))
        item_detail_to_send_to_server = json.dumps({'action': action, 'data': {'user_id':user_id, 'item_id': item_id, 'comment': comment, 'rating': rating}})
        return item_detail_to_send_to_server
    
    def view_next_day_menu(self,user_id):
        action = "VIEW_NEXT_DAY_MENU"
        detail_to_send_to_server = json.dumps({'action': action, "data": {"user_id": user_id}})
        return detail_to_send_to_server
    
    def vote_for_food_item(self,user_id):
        action = "VOTE_FOR_FOOD_ITEM"
        num_items = int(input("Enter number of items you want to vote for: "))
        item_ids = []
        for i in range(num_items):
            item_id = int(input("Enter item id: "))
            item_ids.append(item_id)
        detail_to_send_to_server = json.dumps({'action': action, 'data': {'items_to_vote': item_ids, 'user_id': user_id}})
        return detail_to_send_to_server
    
    def view_notification(self):
        action = "VIEW_NOTIFICATION"
        request_from = "EMPLOYEE"
        item_detail_to_send_to_server = json.dumps({'action': action, 'data': {"request_from": request_from}})
        return item_detail_to_send_to_server
    
    def provide_detailed_feedback(self,user_id):
        action = "PROVIDE_DETAILED_FEEDBACK"
        item_id = int(input("Enter the item_id: "))
        liked = input("What you liked about this item: ")
        disliked = input("What you disliked about this item: ")
        home_recipe = input("Could you please provide your home recipe: ")
        item_detail_to_send_to_server = json.dumps({'action': action, 'data': {'user_id':user_id, 'item_id': item_id, 'liked': liked, 'disliked': disliked, "home_recipe": home_recipe}})
        return item_detail_to_send_to_server
    
    def view_discarded_items(self):
        action = "VIEW_DISCARDED_ITEMS"
        detail_to_send_to_server = json.dumps({'action': action})
        return detail_to_send_to_server
    
    def update_profile(self, user_id):
        action = "UPDATE_PROFILE"
        spice_level = input("Enter your spice level (High, Medium, Low): ")
        dietry = input("Enter your dietry preference (Veg, Non-veg): ")
        item_detail_to_send_to_server = json.dumps({'action': action, 'data': {'user_id':user_id, 'spice_level': spice_level, 'dietry': dietry}})
        return item_detail_to_send_to_server
