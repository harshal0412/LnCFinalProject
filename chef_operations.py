# chef_operations.py
from menu import chef_menu

def send_message(sock, message):
    sock.sendall(message.encode())

def receive_response(sock, buffer_size=4096):
    try:
        response = sock.recv(buffer_size).decode()
        return response
    except Exception as e:
        print(f"Error while receiving response: {e}")
        return ""

def get_menu_recommendations(sock):
    message = "get_menu_recommendations,"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def validate_ids(ids_str):
    try:
        ids = [int(id.strip()) for id in ids_str.split(',') if id.strip().isdigit()]
        if not ids:
            raise ValueError("Empty list of IDs")
        return ids, None
    except ValueError as e:
        return None, str(e)

def roll_out_menu(sock):
    try:
        get_menu_recommendations(sock)
        
        print("\nPlease enter the IDs of the items you want to roll out for each category.")
        
        breakfast_ids_str = input("Enter the menu IDs for breakfast (comma-separated): ").strip()
        lunch_ids_str = input("Enter the menu IDs for lunch (comma-separated): ").strip()
        dinner_ids_str = input("Enter the menu IDs for dinner (comma-separated): ").strip()
        
        # Validate and store breakfast IDs
        ids_str, meal_type = breakfast_ids_str, "breakfast"
        if not ids_str:
            print(f"Invalid input: {meal_type.capitalize()} IDs cannot be empty.")
            return
        
        breakfast_ids, error = validate_ids(ids_str)
        if error:
            print(error)
            return

        # Validate and store lunch IDs
        ids_str, meal_type = lunch_ids_str, "lunch"
        if not ids_str:
            print(f"Invalid input: {meal_type.capitalize()} IDs cannot be empty.")
            return
        
        lunch_ids, error = validate_ids(ids_str)
        if error:
            print(error)
            return

        # Validate and store dinner IDs
        ids_str, meal_type = dinner_ids_str, "dinner"
        if not ids_str:
            print(f"Invalid input: {meal_type.capitalize()} IDs cannot be empty.")
            return
        
        dinner_ids, error = validate_ids(ids_str)
        if error:
            print(error)
            return
        
        message = f"roll_out_menu,{','.join(map(str, breakfast_ids))};{','.join(map(str, lunch_ids))};{','.join(map(str, dinner_ids))}"
        send_message(sock, message)
        response = receive_response(sock)
        print(f"Server response: {response}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

        
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_monthly_report(sock):
    message = "generate_monthly_report,"
    send_message(sock, message)
    response = receive_response(sock)
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
