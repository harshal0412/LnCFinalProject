# chef_operations.py

from menu import chef_menu

def get_menu_recommendations(sock):
    message = "get_menu_recommendations,"
    sock.sendall(message.encode())
    response = sock.recv(4096).decode()  # Adjust buffer size if necessary
    print(response)

def roll_out_menu(sock):
    message = "roll_out_menu,"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)

def generate_monthly_report(sock):
    message = "generate_monthly_report,"
    sock.sendall(message.encode())
    response = sock.recv(4096).decode()  # Adjust buffer size if necessary
    print(response)

def chef_menu_loop(sock):
    while True:
        chef_menu()
        chef_choice = input("Enter your choice (1/2/3/4): ")
        if chef_choice == '1':
            get_menu_recommendations(sock)
        elif chef_choice == '2':
            roll_out_menu(sock)
        elif chef_choice == '3':
            generate_monthly_report(sock)
        elif chef_choice == '4':
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
