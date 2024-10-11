import socket

HOST = "127.0.0.1"
PORT = 8080

# Simple client that takes the input from the user and sends it to the server
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to server with IP:- {HOST}:{PORT}")

    connected = True
    while connected:
        msg = input("Enter your message(If you want to end the connection 'end' to exit): ")

        client.send(msg.encode('utf-8'))

        if msg == "end":
            connected = False
        else:
            msg = client.recv(1024).decode('utf-8')
            print(f"Server received the message: {msg}")

if __name__ == "__main__":
    main()