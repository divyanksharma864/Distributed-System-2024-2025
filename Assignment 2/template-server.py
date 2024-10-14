import socket
from sys import argv
from threading import Thread, Lock
import sys

# this is like shared resource
connected_users = 0
user_lock = Lock()



def handle_client(conn, addr):
    with conn:
        global connected_users
        print(f"Connected by {addr}")
        with user_lock:
            connected_users = connected_users + 1

        while True:
            data = conn.recv(1024)
            message = data.decode()
            print(f"Received: {data.decode()}")

            if message.lower() == "end":
                print(f"Client = {addr} has said to end the connection.")
                break
            
            # if data == b"exit":
            #     break
            conn.sendall(data)  
        # Decrement the user count safely
        with user_lock:
            connected_users = connected_users - 1
        print(f"Closing connection to {addr}")

def operator_commands():
    global connected_users
    while True:
        command = input()
        if command.lower() == "num users":
            with user_lock:
                print(f"Number of connected users: {connected_users}")
        elif command.lower() == "exit":
            print("Shutting down the server.")
            sys.exit(0) 
        else:
            print("Unknown command. Available commands: 'num users', 'exit'")


def main():
    try:
        port = int(argv[1])
    except:
        port = 8080

      # Start the operator thread
    operator_thread = Thread(target=operator_commands)
    operator_thread.start()

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
    print("Server has been shut down.")

if __name__ == "__main__":
    main()
