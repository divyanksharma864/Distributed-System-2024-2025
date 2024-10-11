import socket

HOST = "127.0.0.1"
PORT = 8080

send_data = input("Input the message: ")

# Create a client so that it can connect to server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to server with IP:- {HOST}:{PORT}")
    s.sendall(str.encode(send_data))
    data = s.recv(1024) # data received from server

print(data.decode('utf-8')) # the acknowledgment from the server
