import socket
from sys import argv


def main():
    try:
        port = int(argv[1])
    except:
        port = 8080

    print(f"Server started on port {port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print("Waiting for a client...")

        conn, addr = s.accept()  # Accept a new connection
        with conn:
            print(f"Connected by {addr}") # just to see server is connected to which client
            data = conn.recv(1024)  # Receive data from the client
            if data:
                message_received = data.decode('utf-8')
                print(f"Received message: {message_received}")
        print("Closing connection")


if __name__ == "__main__":
    main()
