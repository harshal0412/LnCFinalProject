from utils.communication import send_message, receive_response

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
    response = receive_response(sock)
    print(response)

def admin_menu_loop(sock):
    from menu import admin_menu
    while True:
        admin_menu()
        choice = input("Enter your choice (1/2/3/4/5): ")
        if choice == '1':
            add_menu_item(sock)
        elif choice == '2':
            update_menu_item(sock)
        elif choice == '3':
            delete_menu_item(sock)
        elif choice == '4':
            display_menu(sock)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
