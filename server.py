#server.py
import socket
from db_operations import DBOperations
from client_handler import ClientHandler

HOST = '127.0.0.1'
PORT = 65432

# Database configuration
db_config = {
    'DRIVER': '{SQL Server}',
    'SERVER': 'ITT-HARSHAL-JA',
    'DATABASE': 'LnC',
    'Trusted_Connection': 'yes'
}

class Server:
    def __init__(self, host, port, db_operations):
        self.host = host
        self.port = port
        self.db_operations = db_operations

    def start(self):
        if not self.db_operations.connection:
            print("Failed to connect to the database")
            return
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._bind_socket(server_socket)
            server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                client_handler = ClientHandler(conn, addr, self.db_operations)
                client_handler.start()

    def _bind_socket(self, server_socket):
        try:
            server_socket.bind((self.host, self.port))
        except PermissionError as e:
            print(f"PermissionError: {e}")
            print("Check if the port is already in use or if you have the necessary permissions.")
            raise

    def stop(self):
        self.db_operations.close()

if __name__ == "__main__":
    db_operations = DBOperations(db_config)
    db_operations.connect()
    
    server = Server(HOST, PORT, db_operations)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print("Server stopped")
    except Exception as e:
        print(f"Server error: {e}")
        server.stop()
