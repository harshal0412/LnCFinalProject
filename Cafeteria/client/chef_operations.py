from utils.communication import send_message, receive_response,validate_ids

def get_menu_recommendations(sock):
    message = "get_menu_recommendations,"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def roll_out_menu(sock):
    try:
        get_menu_recommendations(sock)
        
        print("\nPlease enter the IDs of the items you want to roll out for each category.")
        
        breakfast_ids_str = input("Enter the menu IDs for breakfast (comma-separated): ").strip()
        lunch_ids_str = input("Enter the menu IDs for lunch (comma-separated): ").strip()
        dinner_ids_str = input("Enter the menu IDs for dinner (comma-separated): ").strip()
        
        breakfast_ids, error = validate_ids(breakfast_ids_str)
        if error:
            print(error)
            return

        lunch_ids, error = validate_ids(lunch_ids_str)
        if error:
            print(error)
            return

        dinner_ids, error = validate_ids(dinner_ids_str)
        if error:
            print(error)
            return
        
        message = f"roll_out_menu,{','.join(map(str, breakfast_ids))};{','.join(map(str, lunch_ids))};{','.join(map(str, dinner_ids))}"
        send_message(sock, message)
        response = receive_response(sock)
        print(f"Server response: {response}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def discard_menu_list(sock):
    message = "discard_menu_list"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def generate_monthly_report(sock):
    message = "generate_monthly_report,"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def chef_menu_loop(sock):
    from menu import chef_menu
    while True:
        chef_menu()
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == '1':
            get_menu_recommendations(sock)
        elif choice == '2':
            roll_out_menu(sock)
        elif choice == '3':
            discard_menu_list(sock)
        elif choice == '4':
            generate_monthly_report(sock)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
