import socket
import msgFormat_pb2  # the generated protobuf message class

HOST = "127.0.0.1"
PORT = 8080

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        # taking input from user
        userinput = input("Enter your message, to exit just write exit: ")
        if userinput.lower() == 'exit':
            break 
    
        # protobuf message
        message = msgFormat_pb2.Message()
        message.fr = 1001  # Sender ID
        message.to = 2002  # Receiver ID 2002 i have allocated to server
        message.msg = userinput

        # Serialize the message and send it
        client.send(message.SerializeToString())

        # Receive and decode the echoed message
        data = client.recv(1024)
        echoed_message = msgFormat_pb2.Message()
        echoed_message.ParseFromString(data)

        print(f"Received from server with ID : {echoed_message.to}, Message: {echoed_message.msg}")
    
    client.close()

if __name__ == "__main__":
    main()
