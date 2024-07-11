from client.client import Client
from commons.literals import SERVER_IP, SERVER_PORT
from client.role_based_menu import RoleBasedMenu
import json

def main():
    client = Client(SERVER_IP, SERVER_PORT)
    client.connect()
    try:
        login_and_handle_user(client)
    except KeyboardInterrupt:
        print("Program interrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        client.close()

def login_and_handle_user(client):
    num_tries = 0
    while num_tries < 3:
        email = input("Enter your email to login to the system: ")
        response = client.send_message(email)
        if response == "You are not registered to the system":
            num_tries += 1
            print("Invalid credentials, please try again..!")
            if num_tries >= 3:
                print("Max retry limit reached.")
                return
        else:
            handle_user_session(client, json.loads(response))
            return

def handle_user_session(client, response):
    try:
        user_id, user_role = response[1], response[0].lower()
    except (IndexError, KeyError) as e:
        print(f"Error parsing response: {e}")
        return
    
    if user_role == "admin":
        handle_admin(client)
    elif user_role == "chef":
        handle_chef(client)
    elif user_role == "employee":
        handle_employee(client, user_id)
    else:
        print(f"Unknown role: {user_role}")

def handle_admin(client):
    while True:
        request = RoleBasedMenu.admin_menu()
        if request.lower() == "logout":
            break
        response = safe_send_message(client, request)
        if response:
            process_admin_response(response)

def process_admin_response(response):
    action = response.get('action')
    if action == "ADD_MENU_ITEM":
        print(response['status'])
    elif action == "UPDATE_AVAILABILITY":
        print(response['status'])
    elif action == "DELETE_ITEM":
        print(response['status'])
    elif action == "UPDATE_ITEM_PROPERTY":
        print(response['status'])
    elif action == "VIEW_FEEDBACK":
        print_feedback(response['feedback'])
    elif action == "FETCH_COMPLETE_MENU":
        print_menu(response['data'])

def handle_chef(client):
    while True:
        request = RoleBasedMenu.chef_menu()
        if request.lower() == "logout":
            break
        response = safe_send_message(client, request)
        if response:
            process_chef_response(response)

def process_chef_response(response):
    action = response.get('action')
    if action == "GET_RECOMMENDATION":
        print_recommendations(response['data'])
    elif action == "ROLL_OUT_MENU":
        print(response['status'])
    elif action == "FETCH_COMPLETE_MENU":
        print_menu(response['data'])
    elif action == "VIEW_VOTED_ITEMS":
        print_voted_items(response['data'])
    elif action == "ROLL_OUT_FINALIZED_MENU":
        print(response['status'])
    elif action == "VIEW_NOTIFICATION":
        print_notifications(response['data'])
    elif action == "GENERATE_DISCARD_MENU_ITEM":
        print(response['status'])
    elif action == "REVIEW_DISCARDED_ITEM_LIST":
        print_discarded_items(response['discarded_items'])
    elif action == "DELETE_DISCARDED_ITEMS":
        print(response['status'])
    elif action == "TAKE_DETAILED_FEEDBACK":
        print(response['status'])
    elif action == "VIEW_FEEDBACK":
        print_feedback(response['feedback'])
    elif action == "VIEW_DETAILED_FEEDBACK":
        print_detailed_feedback(response['feedback'])

def handle_employee(client, user_id):
    while True:
        request = RoleBasedMenu.employee_menu(user_id)
        if request.lower() == "logout":
            break
        response = safe_send_message(client, request)
        if response:
            process_employee_response(response)

def process_employee_response(response):
    try:
        action = response.get('action')
        if action == "VIEW_NEXT_DAY_MENU":
            print_menu(response['data']['next_day_menu'])
        elif action == "FETCH_COMPLETE_MENU":
            print_menu(response['data'])
        elif action == "VIEW_NOTIFICATION":
            print_notifications(response['data'])
        elif action == "PROVIDE_FEEDBACK":
            print(response['status'])
        elif action == "VOTE_FOR_FOOD_ITEM":
            print(response['status'])
        elif action == "VIEW_DISCARDED_ITEMS":
            print_discarded_items(response['discarded_items'])
        elif action == "PROVIDE_DETAILED_FEEDBACK":
            print(response['status'])
        elif action == "UPDATE_PROFILE":
            print(response['status'])
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error processing employee response: {e}")
        print(f"Response content: {response}")

def safe_send_message(client, message):
    try:
        response = client.send_message(message)
        return json.loads(response)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error decoding server response: {e}")
    except Exception as e:
        print(f"Error sending message: {e}")
    return None

def print_feedback(feedback):
    if not feedback:
        print("No feedback available.")
        return
    print("User Id".ljust(10), "Item Id".ljust(20), "Comment".ljust(40), "Rating".ljust(40), "Sentiment Score".ljust(0))
    for item in feedback:
        try:
            print(str(item[1]).ljust(10), str(item[2]).ljust(20), str(item[3]).ljust(40), str(item[4]).ljust(40), str(item[5]).ljust(0))
        except IndexError as e:
            print(f"Error printing feedback item: {e}")
            print(f"Feedback item: {item}")

def print_menu(menu):
    if not menu:
        print("No menu items available.")
        return
    print("Item Id".ljust(10), "Item Name".ljust(20), "Price".ljust(20), "Availability Status".ljust(20), "Item Category".ljust(0))
    for item in menu:
        try:
            print(str(item[0]).ljust(10), str(item[1]).ljust(20), str(item[2]).ljust(20), str(item[3]).ljust(20), str(item[4]).ljust(20))
        except IndexError as e:
            print(f"Error printing menu item: {e}")
            print(f"Menu item: {item}")

def print_recommendations(data):
    if not data:
        print("No recommendations available.")
        return
    for category in data:
        print(f"\n----{category.upper()}----")
        print("Item Id".ljust(10), "Item Name".ljust(20), "Price".ljust(20), "Availability Status".ljust(20), "Item Category".ljust(0))
        for item in data[category]:
            try:
                print(str(item[0]).ljust(10), str(item[1]).ljust(20), str(item[2]).ljust(20), str(item[3]).ljust(20), str(item[4]).ljust(20))
            except IndexError as e:
                print(f"Error printing recommendation item: {e}")
                print(f"Recommendation item: {item}")

def print_voted_items(data):
    if not data:
        print("No voted items available.")
        return
    print("Item Id".ljust(10), "User Id".ljust(20))
    for item in data:
        try:
            print(str(item[0]).ljust(10), str(item[1]).ljust(20))
        except IndexError as e:
            print(f"Error printing voted item: {e}")
            print(f"Voted item: {item}")

def print_notifications(data):
    if not data:
        print("No notifications available.")
        return
    for message in data:
        print(message[0])

def print_discarded_items(items):
    if not items:
        print("No discarded items available.")
        return
    print("Item Id".ljust(10), "Item Name".ljust(20), "Average Rating".ljust(20), "Average Sentiment".ljust(20), "Discard list generation date".ljust(0))
    for item in items:
        try:
            print(str(item[0]).ljust(10), str(item[1]).ljust(20), str(item[2]).ljust(20), str(item[3]).ljust(20), str(item[4]).ljust(20))
        except IndexError as e:
            print(f"Error printing discarded item: {e}")
            print(f"Discarded item: {item}")

def print_detailed_feedback(feedback):
    if not feedback:
        print("No employees provided feedback till now")
        return
    print("User Id".ljust(10), "Item Id".ljust(20), "Liked".ljust(40), "Not Liked".ljust(40), "Home Recipe".ljust(0))
    for item in feedback:
        try:
            print(str(item[1]).ljust(10), str(item[2]).ljust(20), str(item[3]).ljust(40), str(item[4]).ljust(40), str(item[5]).ljust(0))
        except IndexError as e:
            print(f"Error printing detailed feedback item: {e}")
            print(f"Detailed feedback item: {item}")

if __name__ == "__main__":
    main()
