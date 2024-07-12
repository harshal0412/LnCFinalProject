def send_message(sock, message):
    try:
        sock.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message: {e}")

def receive_response(sock, buffer_size=1024):
    try:
        response = sock.recv(buffer_size).decode()
        return response
    except Exception as e:
        print(f"Error receiving response: {e}")
        return ""
    
def validate_ids(ids_str):
    try:
        ids = [int(id.strip()) for id in ids_str.split(',') if id.strip().isdigit()]
        if not ids:
            raise ValueError("Empty list of IDs")
        return ids, None
    except ValueError as e:
        return None, str(e)
