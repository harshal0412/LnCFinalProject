import threading
from menu_operations import MenuOperations

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, db):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.db = db
        self.menu_ops = MenuOperations(db)

    def run(self):
        print(f"Connected by {self.addr}")
        with self.conn:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                response = self.handle_request(data.decode())
                self.conn.sendall(response.encode())
        print(f"Connection with {self.addr} closed")

    def handle_request(self, request):
        command, *params = request.split(',')
        print(f"Received command: {command}")
        print(f"Received parameters: {params}")
        
        commands = {
            'signup': self.handle_signup,
            'login': self.handle_login,
            'add_menu_item': self.handle_add_menu_item,
            'update_menu_item': self.handle_update_menu_item,
            'delete_menu_item': self.handle_delete_menu_item,
            'display_menu': self.handle_display_menu,
            'get_menu_recommendations': self.handle_get_menu_recommendations,
            'roll_out_menu': self.handle_roll_out_menu,
            'generate_monthly_report': self.handle_generate_monthly_report,
            'tomorrows_menu': self.handle_tomorrows_menu,
            'give_feedback': self.handle_give_feedback
        }

        handler = commands.get(command, self.handle_invalid_command)
        return handler(params)

    def handle_signup(self, params):
        if len(params) == 3:
            username, password, role = params
            return self.signup(username, password, role)
        return "Invalid signup parameters"

    def handle_login(self, params):
        if len(params) == 2:
            username, password = params
            return self.login(username, password)
        return "Invalid login parameters"

    def handle_add_menu_item(self, params):
        if len(params) == 3:
            name, price, availability = params
            return self.menu_ops.add_menu_item(name, price, availability)
        return "Invalid add menu item parameters"

    def handle_update_menu_item(self, params):
        if len(params) == 3:
            item_id, price, availability = params
            return self.menu_ops.update_menu_item(item_id, price, availability)
        return "Invalid update menu item parameters"

    def handle_delete_menu_item(self, params):
        if len(params) == 1:
            item_id = params[0]
            return self.menu_ops.delete_menu_item(item_id)
        return "Invalid delete menu item parameters"

    def handle_display_menu(self, _):
        return self.menu_ops.display_menu()

    def handle_get_menu_recommendations(self, _):
        return self.menu_ops.get_menu_recommendations()

    def handle_roll_out_menu(self, params):
        params = ','.join(map(str, params))
        try:
            breakfast_str, lunch_str, dinner_str = params.split(';')
            breakfast_ids, error = self.parse_menu_ids(breakfast_str)
            if error:
                return error
            lunch_ids, error = self.parse_menu_ids(lunch_str)
            if error:
                return error
            dinner_ids, error = self.parse_menu_ids(dinner_str)
            if error:
                return error
            return self.menu_ops.roll_out_menu(breakfast_ids, lunch_ids, dinner_ids)
        except ValueError:
            return "Invalid roll out menu parameters: non-integer value"
        except IndexError:
            return "Invalid roll out menu parameters: missing meal categories"

    def handle_generate_monthly_report(self, _):
        return self.menu_ops.generate_monthly_report()

    def handle_tomorrows_menu(self, _):
        return self.menu_ops.tomorrows_menu()

    def handle_give_feedback(self, params):
        if len(params) == 1:
            feedback = params[0]
            return self.menu_ops.give_feedback(feedback)
        return "Invalid feedback parameters"

    def handle_invalid_command(self, _):
        return "Invalid command"

    def signup(self, username, password, role):
        return self.db.signup(username, password, role)

    def login(self, username, password):
        response, role = self.db.login(username, password)
        if response:
            return f"Login successful, role: {role}"
        return "Login failed"

    def parse_menu_ids(self, menu_ids_str):
        try:
            menu_ids = [int(id.strip()) for id in menu_ids_str.split(',')]
            return menu_ids, None
        except ValueError:
            return None, "Invalid roll out menu parameters: non-integer value"
