import socket
from sys import argv
from threading import Thread
from template_pb2 import Message, FastHandshake

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

def listen_for_messages(conn, id):
    while True:
        try:
            msg = receive_message(conn, Message)
            print(f"Received: {msg.msg} from {msg.fr} to {msg.to}")
            if msg.msg == "end":
                print("Server has closed the connection.")
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def main():
    host = "127.0.0.1"
    port = 8080
    try:
        desired_id = int(argv[1]) if len(argv) > 1 else None
    except:
        print("Please provide a numeric client ID")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server")

        # Send the requested ID in the handshake
        handshake = FastHandshake(id=desired_id)
        send_message(s, handshake)
        response = receive_message(s, FastHandshake)

        # Server assigns final ID, error if requested ID is not accepted
        id = response.id
        if response.error:
            print(f"Requested ID {desired_id} was rejected. Using assigned ID {id}")
        else:
            print(f"Successfully connected with ID {id}")

        # Start a thread to listen for incoming messages
        listener_thread = Thread(target=listen_for_messages, args=(s, id))
        listener_thread.start()

        while True:
            data = input("Enter a message (format: '[id] [msg]') or 'end': ")
            if data.lower() == "end":
                msg = Message(fr=id, to=id, msg="end")
                send_message(s, msg)
                break
            try:
                to, msg_content = data.split(" ", 1)
                msg = Message(fr=id, to=int(to), msg=msg_content)
                send_message(s, msg)
            except ValueError:
                print("Invalid input format. Use '[id] [msg]'.")

        print("Closing connection")
        listener_thread.join()  # Wait for the listener thread to finish

if __name__ == "__main__":
    main()
