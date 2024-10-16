import socket
from threading import Thread
import msgFormat_pb2  # the generated protobuf message class

HOST = "127.0.0.1"
PORT = 8080

def client(conn, addr):
    print(f"{addr} has connected.")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        
        # Decode the protobuf message
        message = msgFormat_pb2.Message()
        message.ParseFromString(data)
        
        print(f"Message from {message.fr} to {message.to}: {message.msg}")

        # echoing message back to client 
        conn.send(data)

    conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server is active on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = Thread(target=client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
