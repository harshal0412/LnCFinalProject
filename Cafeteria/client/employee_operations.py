from utils.communication import send_message, receive_response, validate_ids


def tomorrows_menu(sock):
    message = "tomorrows_menu,"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def employee_voting(sock):
    menu_ids_str = input("Enter the menu IDs to increment votes (comma-separated): ").strip()
    if not menu_ids_str:
        print("Invalid input: Menu IDs cannot be empty.")
        return
    
    menu_ids, error = validate_ids(menu_ids_str)
    if error:
        print(error)
        return

    message = f"employee_voting,{','.join(map(str, menu_ids))}"
    send_message(sock, message)
    response = receive_response(sock)
    print(f"Server response: {response}")

def give_feedback(sock):
    menu_id = input("Enter the Menu_id to provide feedback: ")
    feedback = input("Enter your feedback for this menu_item: ")
    rating = input("Enter the rating for this menu_item: ")    
    message = f"give_feedback,{menu_id},{feedback},{rating}"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def employee_menu_loop(sock):
    from menu import employee_menu
    while True:
        employee_menu()
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == '1':
            tomorrows_menu(sock)
        elif choice == '2':
            tomorrows_menu(sock)
            employee_voting(sock)
        elif choice == '3':
            give_feedback(sock)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
 