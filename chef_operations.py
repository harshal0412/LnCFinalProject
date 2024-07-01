#chef_operations.py
from menu import chef_menu

def get_menu_recommendations(sock):
    message = "get_menu_recommendations,"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)

def roll_out_menu(sock):
    try:
        n_breakfast = int(input("Enter the number of breakfast recommendations: "))
        n_lunch = int(input("Enter the number of lunch recommendations: "))
        n_dinner = int(input("Enter the number of dinner recommendations: "))
        message = f"roll_out_menu,{n_breakfast},{n_lunch},{n_dinner}"
        sock.sendall(message.encode())
        response = sock.recv(1024).decode()
        print(response)
    except ValueError:
        print("Invalid input: please enter integer values.")

def generate_monthly_report(sock):
    message = "generate_monthly_report,"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
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
