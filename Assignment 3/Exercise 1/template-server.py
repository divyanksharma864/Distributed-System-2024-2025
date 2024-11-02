import socket
from sys import argv
from threading import Thread
from template_pb2 import Message, FastHandshake

CLIENTS = {}
LAST_ID = 0

def send_message(conn, m):
    serialized = m.SerializeToString()
    conn.sendall(len(serialized).to_bytes(4, byteorder="big"))
    conn.sendall(serialized)

def receive_message(conn, m):
    msg = m()
    size_data = conn.recv(4)
    if not size_data:  # Check if the connection is closed
        return None
    size = int.from_bytes(size_data, byteorder="big")
    data = conn.recv(size)
    msg.ParseFromString(data)
    return msg

def handle_client(conn: socket.socket, addr):
    global LAST_ID
    id = LAST_ID
    LAST_ID += 1

    CLIENTS[id] = (conn, addr)
    with conn:
        handshake = FastHandshake(id=id, error=False)
        send_message(conn, handshake)
        print(f"Connected by #{id} {addr}")

        try:
            # Main communication loop
            while True:
                msg = receive_message(conn, Message)
                
                if msg is None:  # Connection closed by client
                    print(f"Client #{id} disconnected.")
                    break
                
                print(f"Received: {msg.msg} from {msg.fr} to {msg.to}")

                # To check if any client has ended the connection with 'end'
                if msg.msg == "end":
                    print(f"Client #{id} requested disconnection.")
                    break

                # Check if the destination client exists
                if msg.to in CLIENTS:
                    dest_conn, _ = CLIENTS[msg.to]
                    send_message(dest_conn, msg)  # Forward the message to the intended client
                    print(f"Forwarded message from #{msg.fr} to #{msg.to}")
                else:
                    print(f"Message to #{msg.to} dropped (client not found)")
        
        except (ConnectionResetError, ConnectionAbortedError):
            print(f"Client #{id} disconnected unexpectedly.")
        except Exception as e:
            print(f"Error with client #{id}: {e}")
        finally:
            print(f"Closing connection to #{id} {addr}")
            CLIENTS.pop(id, None) 

def loop_main(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", port))
            print(f"Server started on port {port}")
            print("Waiting for a client...")
            s.listen()
            while True:
                try:
                    conn, addr = s.accept()
                    Thread(target=handle_client, args=(conn, addr)).start()
                except KeyboardInterrupt:
                    break
    except Exception as e:
        print(f"Error: {e}")

def main():
    global CLIENTS

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