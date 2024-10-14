import socket
from sys import argv


def main():
    host = "127.0.0.1"
    port = 8080
    try:
        if len(argv) > 2:
            host = argv[1]
            port = int(argv[2])
        elif len(argv) > 1:
            port = int(argv[1])
        else:
            raise ValueError
    except:
        host = "127.0.0.1"
        port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server")
        while True:
            try:
                data = input("Enter a message and to end the talk with server type 'end' = ")
            except:
                data = "end"
            # Send the message to the server
            s.sendall(data.encode())  # Convert message to bytes and send

            print("Message sent")
            if data == "end":
                break
            response = s.recv(1024)
            print(f"Received this from server: {response.decode()}")
        print("Closing connection")


if __name__ == "__main__":
    main()
