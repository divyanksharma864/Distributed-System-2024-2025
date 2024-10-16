import socket
from threading import Thread
import msgFormat_pb2  

HOST = "127.0.0.1"
PORT = 8080

def client(conn, addr):
    print(f"{addr} has connected.")

    # For starting handshake, id and error. Id i have taken same as in exercise 2 for server which is 2002
    handshake = msgFormat_pb2.Handshake()
    handshake.id = 2002  
    handshake.error = False 

     # Sending handshake to the client, server id is same 2002
    conn.send(handshake.SerializeToString())
    print(f"Sent handshake to {addr}: ID={handshake.id}, Error={handshake.error}")

    # Receiving data ie.. handshake Confirmation from Client
    data = conn.recv(1024)
    if not data:
        print(f"No handshake confirmation received from {addr}. Closing the connection.")
        conn.close()
        return
    
    client_handshake = msgFormat_pb2.Handshake()
    client_handshake.ParseFromString(data)
    print(f"Received handshake from {addr}: ID={client_handshake.id}, Error={client_handshake.error}")
    
    if client_handshake.error:
        print(f"Handshake error with {addr}. Closing connection.")
        conn.close()
        return
    else:
        print(f"Handshake successful with {addr}. Now waiting to receive messages.")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        
        message = msgFormat_pb2.Message()
        message.ParseFromString(data)
        
        print(f"Message from {message.fr} to {message.to}: {message.msg}")

        conn.send(data) #data back to client

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
