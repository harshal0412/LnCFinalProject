from menu import chef_menu

def get_menu_recommendations(sock):
    message = "get_menu_recommendations,"
    sock.sendall(message.encode())
    response = sock.recv(4096).decode()  # Increased buffer size for larger messages
    print(response)
    return response

def roll_out_menu(sock):
    try:
        get_menu_recommendations(sock)
        
        print("\nPlease enter the IDs of the items you want to roll out for each category.")
        
        breakfast_ids_str = input("Enter the menu IDs for breakfast (comma-separated): ").strip()
        lunch_ids_str = input("Enter the menu IDs for lunch (comma-separated): ").strip()
        dinner_ids_str = input("Enter the menu IDs for dinner (comma-separated): ").strip()
        
        if not breakfast_ids_str:
            print("Invalid input: Breakfast IDs cannot be empty.")
            return
        if not lunch_ids_str:
            print("Invalid input: Lunch IDs cannot be empty.")
            return
        if not dinner_ids_str:
            print("Invalid input: Dinner IDs cannot be empty.")
            return
        
        def validate_ids(ids_str):
            try:
                print(f"Validating IDs: '{ids_str}'")
                ids = [int(id.strip()) for id in ids_str.split(',')]
                if not ids:
                    raise ValueError("Empty list of IDs")
                print(f"Validated IDs: {ids}")
                return ids, None
            except ValueError as e:
                print(f"Error in validation: {e}")
                return None, "Invalid input: Please enter a comma-separated list of integers."
        
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
        print(f"Sending message: {message}")
        sock.sendall(message.encode())
        response = sock.recv(4096).decode()  # Increased buffer size for larger messages
        print(f"Server response: {response}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_monthly_report(sock):
    message = "generate_monthly_report,"
    sock.sendall(message.encode())
    response = sock.recv(4096).decode()  # Increased buffer size for larger messages
    print(response)

def chef_menu_loop(sock):
    while True:
        chef_menu()
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == '1':
            get_menu_recommendations(sock)
        elif choice == '2':
            roll_out_menu(sock)
        elif choice == '3':
            generate_monthly_report(sock)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
