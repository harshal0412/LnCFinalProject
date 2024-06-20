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
    def __init__(self, host, port, db_config):
        self.host = host
        self.port = port
        self.db = DBOperations()
        self.db.connect(db_config)

    def start(self):
        if not self.db.connection:
            print("Failed to connect to the database")
            return
        
        # Create a TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                client_handler = ClientHandler(conn, addr, self.db)
                client_handler.start()

    def stop(self):
        self.db.close()

if __name__ == "__main__":
    server = Server(HOST, PORT, db_config)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print("Server stopped")
