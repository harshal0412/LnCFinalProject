# authentication_service.py

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
    return response
