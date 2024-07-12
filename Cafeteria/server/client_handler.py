import threading
from database.admin_db_operations import AdminDBOperations
from database.auth_db_operations import AuthDBOperations
from database.chef_db_operations import ChefDBOperations
from database.employee_db_operations import EmployeeDBOperations

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, db):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.db = db
        self.admin_db_ops = AdminDBOperations(db)
        self.auth_db_ops = AuthDBOperations(db)
        self.chef_db_ops = ChefDBOperations(db)
        self.employee_db_ops = EmployeeDBOperations(db)

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
            'discard_menu_list': self.handle_discard_menu_list,
            'tomorrows_menu': self.handle_tomorrows_menu,
            'employee_voting': self.handle_employee_voting,
            'give_feedback': self.handle_give_feedback,
            'increment_votes': self.handle_increment_votes
        }

        handler = commands.get(command, self.handle_invalid_command)
        return handler(params)

    def handle_signup(self, params):
        if len(params) == 3:
            username, password, role = params
            return self.auth_db_ops.signup(username, password, role)
        return "Invalid signup parameters"

    def handle_login(self, params):
        if len(params) == 2:
            username, password = params
            return self.auth_db_ops.login(username, password)
        return "Invalid login parameters"

    def handle_add_menu_item(self, params):
        if len(params) == 3:
            name, price, availability = params
            return self.admin_db_ops.add_menu_item(name, price, availability)
        return "Invalid add menu item parameters"

    def handle_update_menu_item(self, params):
        if len(params) == 3:
            item_id, price, availability = params
            return self.admin_db_ops.update_menu_item(item_id, price, availability)
        return "Invalid update menu item parameters"

    def handle_delete_menu_item(self, params):
        if len(params) == 1:
            item_id = params[0]
            return self.admin_db_ops.delete_menu_item(item_id)
        return "Invalid delete menu item parameters"

    def handle_display_menu(self, params):
        return self.menu_ops.display_menu()

    def handle_get_menu_recommendations(self, params):
        return self.menu_ops.get_menu_recommendations()

    def handle_roll_out_menu(self, params):
        if len(params) == 1:
            breakfast_ids, lunch_ids, dinner_ids = params[0].split(';')
            return self.chef_db_ops.roll_out_menu(breakfast_ids, lunch_ids, dinner_ids)
        return "Invalid roll out menu parameters"

    def handle_generate_monthly_report(self, params):
        return self.chef_db_ops.generate_monthly_report()

    def handle_discard_menu_list(self, params):
        return self.chef_db_ops.discard_menu_list()

    def handle_tomorrows_menu(self, params):
        return self.chef_db_ops.tomorrows_menu()

    def handle_employee_voting(self, params):
        return self.employee_db_ops.employee_voting()

    def handle_give_feedback(self, params):
        return self.employee_db_ops.give_feedback()

    def handle_increment_votes(self, params):
        return self.employee_db_ops.increment_votes()

    def handle_invalid_command(self, params):
        return "Invalid command"
