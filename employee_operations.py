# employee_operations.py

from menu import employee_menu

def tomorrows_menu(sock):
    message = "tomorrows_menu,"
    sock.sendall(message.encode())
    response = sock.recv(4096).decode()  # Adjust buffer size if necessary
    print(response)

def give_feedback(sock, feedback):
    message = f"give_feedback,{feedback}"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)

def employee_menu_loop(sock):
    while True:
        employee_menu()
        employee_choice = input("Enter your choice (1/2/3): ")
        if employee_choice == '1':
            tomorrows_menu(sock)
        elif employee_choice == '2':
            feedback = input("Enter your feedback: ")
            give_feedback(sock, feedback)
        elif employee_choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
