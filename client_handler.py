# client_handler.py

import threading
from menu_operations import MenuOperations
from admin_operations import admin_menu_loop
from employee_operations import employee_menu_loop
from chef_operations import chef_menu_loop

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, db):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.db = db
        self.menu_ops = MenuOperations(db)

    def signup(self, username, password, role):
        response = self.db.signup(username, password, role)
        return response

    def login(self, username, password):
        response, role = self.db.login(username, password)
        if response:
            return f"Login successful, role: {role}"
        else:
            return "Login failed"

    def handle_admin_menu(self):
        admin_menu_loop(self.conn)  # Pass the socket to the admin menu loop function
        return "Admin menu session ended"

    def handle_employee_menu(self):
        employee_menu_loop(self.conn)  # Pass the socket to the employee menu loop function
        return "Employee menu session ended"

    def handle_chef_menu(self):
        chef_menu_loop(self.conn)  # Pass the socket to the chef menu loop function
        return "Chef menu session ended"

    def run(self):
        print(f"Connected by {self.addr}")
        with self.conn:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                command, *params = data.decode().split(',')
                if command == 'signup':
                    if len(params) == 3:
                        username, password, role = params
                        response = self.signup(username, password, role)
                    else:
                        response = "Invalid signup parameters"
                elif command == 'login':
                    if len(params) == 2:
                        username, password = params
                        response = self.login(username, password)
                    else:
                        response = "Invalid login parameters"
                elif command == 'add_menu_item':
                    if len(params) == 3:
                        name, price, availability = params
                        response = self.menu_ops.add_menu_item(name, price, availability)
                    else:
                        response = "Invalid add menu item parameters"
                elif command == 'update_menu_item':
                    if len(params) == 3:
                        item_id, price, availability = params
                        response = self.menu_ops.update_menu_item(item_id, price, availability)
                    else:
                        response = "Invalid update menu item parameters"        
                elif command == 'delete_menu_item':
                    if len(params) == 1:
                        item_id = params[0]
                        response = self.menu_ops.delete_menu_item(item_id)
                    else:
                        response = "Invalid delete menu item parameters"
                elif command == 'admin_menu':
                    response = self.handle_admin_menu()
                elif command == 'employee_menu':
                    response = self.handle_employee_menu()
                elif command == 'chef_menu':
                    response = self.handle_chef_menu()
                else:
                    response = "Invalid command"
                
                self.conn.sendall(response.encode())
        
        print(f"Connection with {self.addr} closed")
