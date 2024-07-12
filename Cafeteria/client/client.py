import sys
import os
import socket

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now import your modules
from utils.communication import send_message, receive_response
from utils.menu import menu

HOST = '127.0.0.1'
PORT = 65432

def connect_to_server():
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
    if role_response.startswith("Login successful, role:"):
        print(role_response)
        response = role_response.split(':')[1].strip()
        role = response.split(',')[0].strip()
        if role == 'admin':
            from admin_operations import admin_menu_loop
            admin_menu_loop(s)
        elif role == 'chef':
            from chef_operations import chef_menu_loop
            chef_menu_loop(s)
        elif role == 'employee':
            from employee_operations import employee_menu_loop
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
                from authentication_service import signup
                signup(s)
            elif choice == '2':
                from authentication_service import login
                login_response = login(s)
                handle_login_response(login_response, s)
            elif choice == '3':
                print("Closing connection")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    finally:
        s.close()

if __name__ == "__main__":
    main()
