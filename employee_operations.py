# employee_operations.py

from menu import employee_menu

def tomorrows_menu(sock):
    message = "tomorrows_menu,"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)

def give_feedback(sock):
    feedback = input("Enter your feedback: ")
    message = f"give_feedback,{feedback}"
    sock.sendall(message.encode())
    response = sock.recv(1024).decode()
    print(response)

def employee_menu_loop(sock):
    while True:
        employee_menu()
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            tomorrows_menu(sock)
        elif choice == '2':
            give_feedback(sock)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
