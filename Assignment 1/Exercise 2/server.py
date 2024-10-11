import socket

HOST = "127.0.0.1"
PORT = 8080

# Creating a socket and binding it and listening the client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()  
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()  
    # listening for the message and print it and sending back acknowledgment
    with conn:
        print(f"Connected to {addr}")
        while True:
            # Receive data from client
            data = conn.recv(1024)
            if not data:
                break  
            
            print("Received your message client: ", data.decode('utf-8') )

            # Sending an acknowledgment back to the client that server received your message
            reply_message = "Message received to server: " + data.decode('utf-8')
            conn.sendall(reply_message.encode('utf-8'))
            conn.sendall(str.encode("Server will now close the connection"))

        print("Closing connection with client.")
