# employee_operations.py
from menu import employee_menu

def send_message(sock, message):
    sock.sendall(message.encode())

def receive_response(sock, buffer_size=1024):
    try:
        response = sock.recv(buffer_size).decode()
        return response
    except Exception as e:
        print(f"Error while receiving response: {e}")
        return ""

def tomorrows_menu(sock):
    message = "tomorrows_menu,"
    send_message(sock, message)
    response = receive_response(sock)
    print(response)

def give_feedback(sock):
    feedback = input("Enter your feedback: ")
    message = f"give_feedback,{feedback}"
    send_message(sock, message)
    response = receive_response(sock)
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
