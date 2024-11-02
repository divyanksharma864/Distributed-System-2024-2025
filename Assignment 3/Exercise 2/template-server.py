import socket
from sys import argv
from threading import Thread
from template_pb2 import Message, FastHandshake

CLIENTS = {}
LAST_ID = 0
message_buffer = {}  # Store undelivered messages for offline clients

def send_message(conn, m):
    serialized = m.SerializeToString()
    conn.sendall(len(serialized).to_bytes(4, byteorder="big"))
    conn.sendall(serialized)

def receive_message(conn, m):
    msg = m()
    size = int.from_bytes(conn.recv(4), byteorder="big")
    data = conn.recv(size)
    msg.ParseFromString(data)
    return msg

def handle_client(conn: socket.socket, addr):
    global LAST_ID
    id = LAST_ID  # Default ID assignment
    LAST_ID += 1

    try:
        # Receive handshake with requested ID
        handshake_request = receive_message(conn, FastHandshake)
        requested_id = handshake_request.id

        # Check if the requested ID is available
        if requested_id not in CLIENTS:
            id = requested_id
        else:
            print(f"Requested ID {requested_id} is already in use. Using default ID {id}")

        CLIENTS[id] = (conn, addr)
        handshake = FastHandshake(id=id, error=(id != requested_id))
        send_message(conn, handshake)

        print(f"Connected by #{id} {addr}")

        # Send buffered messages if any
        if id in message_buffer:
            for buffered_msg in message_buffer[id]:
                send_message(conn, buffered_msg)
            del message_buffer[id]  # Clear buffer for this client

        # Main communication loop
        while True:
            msg = receive_message(conn, Message)
            print(f"Received: {msg.msg} from {msg.fr} to {msg.to}")

            # Check if the receiver is connected
            if msg.to in CLIENTS:
                receiver_conn, _ = CLIENTS[msg.to]
                send_message(receiver_conn, msg)
            else:
                # Buffer the message for offline clients
                if msg.to not in message_buffer:
                    message_buffer[msg.to] = []
                message_buffer[msg.to].append(msg)
                print(f"Buffered message for client #{msg.to}")

            if msg.msg == "end":
                print(f"Client #{id} requested disconnection.")
                break  # Exit the loop if the client sends "end"

        print(f"Closing connection to #{id} {addr}")
        CLIENTS.pop(id)  # Remove client from the active list

    except (ConnectionResetError, ConnectionAbortedError):
        print(f"Client #{id} disconnected unexpectedly.")
    except Exception as e:
        print(f"Error with client #{id}: {e}")
    finally:
        conn.close()

def loop_main(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", port))
            print(f"Server started on port {port}")
            print("Waiting for a client...")
            s.listen()
            while True:
                conn, addr = s.accept()
                Thread(target=handle_client, args=(conn, addr)).start()
    except Exception as e:
        print(f"Server error: {e}")

def main():
    try:
        port = int(argv[1])
    except:
        port = 8080

    loop = Thread(target=loop_main, args=(port,))
    loop.daemon = True
    loop.start()

    while True:
        try:
            command = input("op> ").strip().lower()
        except:
            break

        if command == "num_users":
            print(f"Number of users: {len(CLIENTS)}")
        else:
            print("Invalid command")
            print("Available commands:")
            print("- num_users: Get the number of connected users")

if __name__ == "__main__":
    main()
