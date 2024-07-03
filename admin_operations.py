# admin_operations.py
from menu import admin_menu

def send_message(sock, message):
    sock.sendall(message.encode())

def receive_response(sock, buffer_size=1024):
    try:
        response = sock.recv(buffer_size).decode()
        return response
    except Exception as e:
        print(f"Error while receiving response: {e}")
        return ""

def add_menu_item(sock):
    name = input("Enter menu item name: ")
    price = input("Enter menu item price: ")
    availability = input("Is the item available (True/False): ")

    message = f"add_menu_item,{name},{price},{availability}"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def update_menu_item(sock):
    item_id = input("Enter menu item ID to update: ")
    price = input("Enter new menu item price: ")
    availability = input("Is the item available (True/False): ")

    message = f"update_menu_item,{item_id},{price},{availability}"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def delete_menu_item(sock):
    item_id = input("Enter menu item ID to delete: ")
    message = f"delete_menu_item,{item_id}"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def display_menu(sock):
    message = "display_menu,"
    send_message(sock, message)
    response = receive_response(sock, buffer_size=4096)
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
