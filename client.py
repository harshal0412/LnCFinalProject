import socket

# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def menu():
    print("Menu:")
    print("1. Signup")
    print("2. Login")
    print("3. Exit")

def signup(sock):
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/chef/employee): ")
    message = f"signup,{username},{password},{role}"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)

def login(sock):
    username = input("Enter username: ")
    password = input("Enter password: ")
    message = f"login,{username},{password}"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
        
        while True:
            menu()
            choice = input("Enter your choice (1/2/3): ")
            
            if choice == '1':
                signup(s)
            elif choice == '2':
                login(s)
            elif choice == '3':
                print("Closing connection")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        # Close the socket
        s.close()

if __name__ == "__main__":
    main()
