import socket
import msgFormat_pb2

HOST = "127.0.0.1"
PORT = 8080

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Receiving handshake from server
    data = client.recv(1024)
    if not data:
        print("No handshake got from server")
        client.close()
        return
    
    server_handshake = msgFormat_pb2.Handshake()
    server_handshake.ParseFromString(data)
    print(f"Received handshake from server: ID={server_handshake.id}, Error={server_handshake.error}")
    
    if server_handshake.error:
        print("Server reported an error during handshake. Exiting.")
        client.close()
        return
    else:
        print("Great handshake successful with server.")
    
    # Send Handshake Confirmation to Server
    client_handshake = msgFormat_pb2.Handshake()
    client_handshake.id = 1001 
    client_handshake.error = False  
    client.send(client_handshake.SerializeToString())
    print(f"Sent handshake confirmation to server: ID={client_handshake.id}, Error={client_handshake.error}")
        

    while True:
        userinput = input("Enter your message, to exit just write exit: ")
        if userinput.lower() == 'exit':
            break 
    
        message = msgFormat_pb2.Message()
        message.fr = 1001  
        message.to = 2002  # Receiver ID 2002 i have allocated to server
        message.msg = userinput

        client.send(message.SerializeToString())

        data = client.recv(1024)
        echoed_message = msgFormat_pb2.Message()
        echoed_message.ParseFromString(data)

        print(f"Received from server with ID = {echoed_message.to}, Message is = {echoed_message.msg}")
    
    client.close()

if __name__ == "__main__":
    main()
