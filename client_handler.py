import threading

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, db):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.db = db

    def run(self):
        print(f"Connected by {self.addr}")
        with self.conn:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                command, *params = data.decode().split(',')
                if command == 'signup':
                    username, password, role = params
                    response = self.db.signup(username, password, role)
                elif command == 'login':
                    username, password = params
                    response = self.db.login(username, password)
                else:
                    response = "Invalid command"
                self.conn.sendall(response.encode())
        print(f"Connection with {self.addr} closed")
