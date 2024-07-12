import sys
import os

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import socket
from database.admin_db_operations import AdminDBOperations
from database.chef_db_operations import ChefDBOperations
from database.employee_db_operations import EmployeeDBOperations
from client_handler import ClientHandler

HOST = '127.0.0.1'
PORT = 65432

# Database configurations
admin_db_config = {
    'DRIVER': '{SQL Server}',
    'SERVER': 'ITT-HARSHAL-JA',
    'DATABASE': 'AdminDB',
    'Trusted_Connection': 'yes'
}

chef_db_config = {
    'DRIVER': '{SQL Server}',
    'SERVER': 'ITT-HARSHAL-JA',
    'DATABASE': 'ChefDB',
    'Trusted_Connection': 'yes'
}

employee_db_config = {
    'DRIVER': '{SQL Server}',
    'SERVER': 'ITT-HARSHAL-JA',
    'DATABASE': 'EmployeeDB',
    'Trusted_Connection': 'yes'
}

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._bind_socket(server_socket)
            server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                client_thread = self._create_client_handler(conn, addr)
                client_thread.start()

    def _bind_socket(self, server_socket):
        try:
            server_socket.bind((self.host, self.port))
        except PermissionError as e:
            print(f"PermissionError: {e}")
            print("Check if the port is already in use or if you have the necessary permissions.")
            raise

    def _create_client_handler(self, conn, addr):
        # Replace with actual logic to determine client role
        role = "admin"  # Example: You should determine this dynamically

        if role == "admin":
            db_operations = AdminDBOperations(admin_db_config)
        elif role == "chef":
            db_operations = ChefDBOperations(chef_db_config)
        elif role == "employee":
            db_operations = EmployeeDBOperations(employee_db_config)
        else:
            raise ValueError("Unknown role")

        return ClientHandler(conn, addr, db_operations)

if __name__ == "__main__":
    server = Server(HOST, PORT)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopped")
