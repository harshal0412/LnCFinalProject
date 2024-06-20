# admin_operations.py

from menu import admin_menu

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

def display_menu(sock):
    message = "display_menu,"
    sock.sendall(message.encode())
    response = sock.recv(4096).decode()  # Adjust buffer size if necessary
    print(response)

def admin_menu_loop(sock):
    while True:
        admin_menu()
        admin_choice = input("Enter your choice (1/2/3/4/5): ")
        if admin_choice == '1':
            add_menu_item(sock)
        elif admin_choice == '2':
            update_menu_item(sock)
        elif admin_choice == '3':
            delete_menu_item(sock)
        elif admin_choice == '4':
            display_menu(sock)
        elif admin_choice == '5':
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
