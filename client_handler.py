import threading
import db_operations

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, db):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.db = db

    def signup(self, username, password, role):
        response = self.db.signup(username, password, role)
        return response

    def login(self, username, password):
        response = self.db.login(username, password)
        return response

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
                else:
                    response = "Invalid command"
                
                self.conn.sendall(response.encode())
        
        print(f"Connection with {self.addr} closed")
