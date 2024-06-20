import socket

# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def menu():
    print("Menu:")
    print("1. Signup")
    print("2. Login")
    print("3. Exit")

def admin_menu():
    print("Admin Menu:")
    print("1. Add Menu Item")
    print("2. Update Menu Item")
    print("3. Delete Menu Item")
    print("4. Logout")

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

def add_menu_item(sock):
    name = input("Enter menu item name: ")
    price = input("Enter menu item price: ")
    availability = input("Is the item available (yes/no): ")
    message = f"add_menu_item,{name},{price},{availability}"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)

def update_menu_item(sock):
    item_id = input("Enter menu item ID to update: ")
    price = input("Enter new menu item price: ")
    availability = input("Is the item available (yes/no): ")
    message = f"update_menu_item,{item_id},{price},{availability}"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)



def delete_menu_item(sock):
    item_id = input("Enter menu item ID to delete: ")
    message = f"delete_menu_item,{item_id}"
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
                role_response = login(s)
                if role_response.startswith("Login successful, role:"):
                    role = role_response.split(':')[1].strip()
                    if role == 'admin':
                        while True:
                            admin_menu()
                            admin_choice = input("Enter your choice (1/2/3/4): ")
                            if admin_choice == '1':
                                add_menu_item(s)
                            elif admin_choice == '2':
                                update_menu_item(s)
                            elif admin_choice == '3':
                                delete_menu_item(s)
                            elif admin_choice == '4':
                                break
                            else:
                                print("Invalid choice. Please enter 1, 2, 3, or 4.")
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
