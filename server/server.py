import socket
import threading
import sys
sys.path.append("..")
from client_handler import ClientHandler
from commons.literals import SERVER_IP, SERVER_PORT

class Server:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self):
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.server_ip}:{self.server_port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_handler = ClientHandler(client_socket, client_address)
            client_thread = threading.Thread(target=client_handler.handle)
            client_thread.start()

if __name__ == "__main__":
    server = Server(SERVER_IP, SERVER_PORT)
    server.start()
