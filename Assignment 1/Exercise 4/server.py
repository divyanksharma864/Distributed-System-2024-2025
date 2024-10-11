import threading
import socket

HOST = "127.0.0.1"
PORT = 8080

def uptouclient(conn, addr):
    print(f"{addr} has connected to the server.")

    connected  = True
    while connected:
        data = conn.recv(1024)
        message = data.decode('utf-8')
        if message == "end":
            connected = False
            print(f"{addr} has disconnected")
        print(f"Message from {addr}: {message}")
        conn.send(message.encode('utf-8'))
    conn.close

def main():
    # now creating the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    # now every new client will be allocated to the thread and then till its connected it will be handeled by uptouclient function
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=uptouclient, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()

