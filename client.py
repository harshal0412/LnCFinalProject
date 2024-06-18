import socket
import threading

HOST = '127.0.0.1'  
PORT = 65432        

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(f"Received from server: {data.decode()}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
        
        # Start a thread to listen for incoming messages
        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.start()

        while True:
            command = input("Enter command (signup/login): ")
            if command == 'signup':
                username = input("Enter username: ")
                password = input("Enter password: ")
                role = input("Enter role (admin/chef/Employee): ")
                message = f"{command},{username},{password},{role}"
            elif command == 'login':
                username = input("Enter username: ")
                password = input("Enter password: ")
                message = f"{command},{username},{password}"
            else:
                print("Invalid command")
                continue

            if command.lower() == 'quit':
                print("Closing connection")
                break
            
            s.sendall(message.encode())

        s.close()

if __name__ == "__main__":
    main()
