# client.py

import socket
from menu import menu
from authentication_service import signup, login

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

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
                role_response = login(s)
                if role_response.startswith("Login successful, role:"):
                    role = role_response.split(':')[1].strip()
                    if role == 'admin':
                        from admin_operations import admin_menu_loop
                        admin_menu_loop(s)
                    else:
                        print(f"Login successful, role: {role}")
            elif choice == '3':
                print("Closing connection")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        
        # Close the socket
        s.close()

if __name__ == "__main__":
    main()
