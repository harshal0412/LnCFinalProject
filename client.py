import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(f"Received from server: {data.decode()}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
        
        # Start a thread to listen for incoming messages
        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.start()

        while True:
            message = input("Enter message to send (type 'quit' to exit): ")
            if message.lower() == 'quit':
                print("Closing connection")
                break
            
            s.sendall(message.encode())
        
        # Close the socket
        s.close()

if __name__ == "__main__":
    main()
