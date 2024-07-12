from utils.communication import send_message, receive_response

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
    send_message(sock, message)

    response = receive_response(sock)
    print(response)

def login(sock):
    username = get_user_input("Enter username: ")
    password = get_user_input("Enter password: ")

    message = f"login,{username},{password}"
    send_message(sock, message)

    response = receive_response(sock)
    print(response)
    return response
