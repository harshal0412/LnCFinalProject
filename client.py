import socket
from menu import menu
from authentication_service import signup, login
from admin_operations import admin_menu_loop
from chef_operations import chef_menu_loop
from employee_operations import employee_menu_loop

HOST = '127.0.0.1'
PORT = 65432

def connect_to_server():
    """
    Establishes a connection to the server.
    Returns the socket object on success, None on failure.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
        return s
    except ConnectionRefusedError:
        print(f"Connection to {HOST}:{PORT} refused. Please check the server.")
    except Exception as e:
        print(f"Connection error: {e}")
    return None

def handle_login_response(role_response, s):
    """
    Handles the role response after successful login.
    """
    if role_response.startswith("Login successful, role:"):
        print(role_response)
        reponse = role_response.split(':')[1].strip()        
        role = reponse.split(',')[0].strip()
        Emp_id =reponse.split(',')[1].strip()
        if role == 'admin':
            admin_menu_loop(s)
        elif role == 'chef':
            chef_menu_loop(s)
        elif role == 'employee':
            employee_menu_loop(s)
    else:
        print("Login failed")

def main():
    s = connect_to_server()
    if not s:
        return

    try:
        while True:
            menu()
            choice = input("Enter your choice (1/2/3): ").strip()

            if choice == '1':
                signup(s)
            elif choice == '2':
                role_response = login(s)
                handle_login_response(role_response, s)
            elif choice == '3':
                print("Closing connection")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    finally:
        s.close()

if __name__ == "__main__":
    main()
