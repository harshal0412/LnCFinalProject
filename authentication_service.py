# authentication_service.py

def get_user_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input

def signup(sock):
    username = get_user_input("Enter username: ")
    password = get_user_input("Enter password: ")
    role = get_user_input("Enter role (admin/chef/employee): ")

    message = f"signup,{username},{password},{role}"
    sock.sendall(message.encode())

    try:
        response = sock.recv(1024).decode()
        print(response)
    except Exception as e:
        print(f"Error while receiving response: {e}")

def login(sock):
    username = get_user_input("Enter username: ")
    password = get_user_input("Enter password: ")

    message = f"login,{username},{password}"
    sock.sendall(message.encode())

    try:
        response = sock.recv(1024).decode()
        print(response)
        return response
    except Exception as e:
        print(f"Error while receiving response: {e}")
        return ""
