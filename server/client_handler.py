import json
import sys
from services.chef_service import ChefService
from services.discard_menu_item import DiscardMenu
from services.employee_service import EmployeeService
from services.feedback_service import Feedback
from services.notification_service import Notification
from services.admin_service import AdminService
sys.path.append("..")
from services.authentication import AuthService
from services.menu_item import MenuItem

class ClientHandler:
    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address

    def handle(self):
        print(f"Accepted connection from {self.client_address}")
        try:
            email = self.client_socket.recv(1024).decode('utf-8')
            authenticate_user = AuthService()
            user_details = authenticate_user.login(email)
            if len(user_details) == 1:
                user_role = user_details[0][2]
                user_id = user_details[0][3]
                self.client_socket.send(json.dumps([user_role,user_id]).encode('utf-8'))
                while True:
                    data = self.client_socket.recv(1024)
                    if not data:
                        break
                    request = json.loads(data)
                    if(request['action'] == "ADD_MENU_ITEM"):
                        admin_service = AdminService()
                        response = admin_service.add_menu_item(request['data'], request['item_property'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "UPDATE_AVAILABILITY"):
                        admin_service = AdminService()
                        response = admin_service.update_item_availability(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "DELETE_ITEM"):
                        admin_service = AdminService()
                        response = admin_service.delete_item_from_menu(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "UPDATE_ITEM_PROPERTY"):
                        admin_service = AdminService()
                        response = admin_service.update_item_properties(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "FETCH_COMPLETE_MENU"):
                        response = MenuItem.fetch_complete_menu()
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "GET_RECOMMENDATION"):
                        chef_service = ChefService()
                        response = chef_service.get_recommendation(request['number_of_items_chef_want'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "ROLL_OUT_MENU"):
                        chef_service = ChefService()
                        response = chef_service.roll_out_menu(request['items_to_rollout'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "ROLL_OUT_FINALIZED_MENU"):
                        chef_service = ChefService()
                        response = chef_service.roll_out_finalized_menu(request['items_to_rollout'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "VIEW_VOTED_ITEMS"):
                        chef_service = ChefService()
                        response = chef_service.view_voted_items(request['date'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "GENERATE_DISCARD_MENU_ITEM"):
                        discard_item = DiscardMenu()
                        response = discard_item.add_items_to_discard_list()
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "REVIEW_DISCARDED_ITEM_LIST"):
                        discard_item = DiscardMenu()
                        response = discard_item.review_discarded_item_list()
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "TAKE_DETAILED_FEEDBACK"):
                        chef_service = ChefService()
                        response = chef_service.take_detailed_feedback()
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "VIEW_DETAILED_FEEDBACK"):
                        feedback = Feedback()
                        response = feedback.get_feedback("detailed")
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "VIEW_FEEDBACK"):
                        feedback = Feedback()
                        response = feedback.get_feedback()
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "DELETE_DISCARDED_ITEMS"):
                        chef_service = ChefService()
                        response = chef_service.delete_discarded_items(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "VIEW_NOTIFICATION"):
                        notification = Notification()
                        response = notification.view_notification(request['data']['request_from'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "PROVIDE_FEEDBACK"):
                        feedback = Feedback()
                        response = feedback.provide_feedback(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "PROVIDE_DETAILED_FEEDBACK"):
                        feedback = Feedback()
                        response = feedback.provide_detailed_feedback(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "VIEW_NEXT_DAY_MENU"):
                        next_day_menu = MenuItem()
                        response = next_day_menu.view_next_day_menu(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "VOTE_FOR_FOOD_ITEM"):
                        employee_service = EmployeeService()
                        response = employee_service.vote_for_food_item(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "VIEW_DISCARDED_ITEMS"):
                        employee_service = EmployeeService()
                        response = employee_service.view_discarded_items()
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "UPDATE_PROFILE"):
                        employee_service = EmployeeService()
                        response = employee_service.update_profile(request['data'])
                        self.client_socket.send(json.dumps(response).encode('utf-8'))
                    elif(request['action'] == "EMPLOYEE_VIEW_NOTIFICATION"):
                        employee_service = EmployeeService()
                        notification = employee_service.view_notification()
                        if(notification == "Error in fetching notification"):
                            self.client_socket.send(notification.encode('utf-8'))
                        else:
                            self.client_socket.send(json.dumps(notification).encode('utf-8'))
            else:
                print(f"User Not Authenticated")
                response = "You are not registered to the system"
                self.client_socket.send(response.encode('utf-8'))
        except (ConnectionResetError, ConnectionAbortedError):
            pass
        finally:
            print(f"Connection from {self.client_address} has been closed")
            self.client_socket.close()
