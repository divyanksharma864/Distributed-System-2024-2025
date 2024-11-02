import socket
from sys import argv
from threading import Thread
from template_pb2 import Message, FastHandshake

def send_message(conn, msg_obj):
    """Serializes and sends a protobuf message over the connection."""
    serialized = msg_obj.SerializeToString()
    conn.sendall(len(serialized).to_bytes(4, byteorder="big"))
    conn.sendall(serialized)

def receive_message(conn, msg_type):
    """Receives a message of a given protobuf type over the connection."""
    msg = msg_type()
    size = int.from_bytes(conn.recv(4), byteorder="big")
    data = conn.recv(size)
    msg.ParseFromString(data)
    return msg

def listen_for_messages(conn, client_id):
    """Continuously listens for incoming messages from the server."""
    while True:
        try:
            received_msg = receive_message(conn, Message)
            print(f"\nReceived: {received_msg.msg} from {received_msg.fr} to {received_msg.to}")
        except Exception:
            print(f"\nConnection closed by server for client #{client_id}")
            break

def parse_arguments():
    """Parses command-line arguments to get host and port, with defaults."""
    default_host = "127.0.0.1"
    default_port = 8080

    if len(argv) > 2:
        return argv[1], int(argv[2])
    elif len(argv) > 1:
        return default_host, int(argv[1])
    else:
        return default_host, default_port

def main():
    host, port = parse_arguments()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server")

        # Initial handshake to retrieve client ID
        handshake = receive_message(s, FastHandshake)
        if handshake.error:
            print("Server rejected the connection")
            return

        client_id = handshake.id
        print(f"We are client #{client_id}")

        # Start a thread to listen for incoming messages
        listener_thread = Thread(target=listen_for_messages, args=(s, client_id), daemon=True)
        listener_thread.start()

        while True:
            try:
                data = input("Enter a message (format: [id] [msg]): ")
            except EOFError:
                data = "end"

            if data.lower() == "end":
                # Send an "end" message to self, signaling to terminate the connection
                end_msg = Message(fr=client_id, to=client_id, msg="end")
                send_message(s, end_msg)
                break

            # Parse input to get recipient ID and message content
            parts = data.split(" ", 1)
            if len(parts) < 2:
                print("Invalid input format. Use [id] [msg].")
                continue

            try:
                recipient_id = int(parts[0])
                message_content = parts[1]
            except ValueError:
                print("Invalid recipient ID format. Please enter a valid integer.")
                continue

            msg = Message(fr=client_id, to=recipient_id, msg=message_content)
            send_message(s, msg)

        print("Closing connection")

if __name__ == "__main__":
    main()
