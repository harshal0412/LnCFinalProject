import socket
from db_operations import Database
from client_handler import ClientHandler

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

# Database configuration
db_config = {
    'DRIVER': '{SQL Server}',
    'SERVER': 'ITT-HARSHAL-JA',  # Replace with your SQL Server name
    'DATABASE': 'LnC',
    'Trusted_Connection': 'yes'
}

class Server:
    def __init__(self, host, port, db_config):
        self.host = host
        self.port = port
        self.db = Database(db_config)

    def start(self):
        self.db.connect()
        if not self.db.connection:
            print("Failed to connect to the database")
            return
        
        #TCP socket (socket.socket) for IPv4 (AF_INET) and TCP (SOCK_STREAM).
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server listening on {self.host}:{self.port}")

            #s.accept() blocking method that waits until a client connects to the server returns connection and address
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
